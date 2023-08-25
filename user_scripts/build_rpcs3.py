import sys
import os
import subprocess
import shutil
import psutil

sys.path.append("../dependencies/dev_scripts")

from build_ark import build_patch_ark
from download_mackiloha import download_mackiloha

# List of required packages
required_packages = ["psutil"]

# Check if the system is running on macOS
is_macos = sys.platform == "darwin"

# Check if each package is installed, and if not, install it
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Installing...")
        
        # Use "pip3" on macOS and Linux, and "pip" on Windows
        pip_command = "pip3" if is_macos or sys.platform.startswith("linux") else "pip"
        
        subprocess.check_call([pip_command, "install", package])

def run_in_detached_process(command):
    subprocess.Popen(command, close_fds=True)

def close_rpcs3_process_windows():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'rpcs3.exe':
            print(f"Terminating rpcs3.exe (PID: {process.info['pid']})")
            process.terminate()
            process.wait()  # Wait for the process to terminate
            break

def close_rpcs3_process_mac():
    for process in psutil.process_iter(['pid', 'name']):
        process_name = process.info['name']
        if process_name.lower() == 'rpcs3':
            print(f"Terminating {process_name} (PID: {process.info['pid']})")
            process.terminate()
            process.wait()  # Wait for the process to terminate
            break


# Function to ask for the rpcs3 dev_hdd0 directory and save it to a file
def get_rpcs3_directory():
    directory_file = "rpcs3_directory.txt"
    if os.path.exists(directory_file):
        with open(directory_file, "r") as file:
            rpcs3_directory = file.readline().strip()
            if is_macos:
                # Remove any leading/trailing quotes and whitespace
                rpcs3_directory = rpcs3_directory.strip('"\' ')
            if is_macos:
                # Replace escaped backslashes with regular slashes
                rpcs3_directory = rpcs3_directory.replace("\\", "")

            if rpcs3_directory and validate_rpcs3_directory(rpcs3_directory):
                return rpcs3_directory
            else:
                print("Stored rpcs3_directory is not valid. Please enter the path again.")
                return input("Please enter the path to your rpcs3 dev_hdd0 directory: ")
    

    while True:
        rpcs3_directory = input("Please enter the path to your rpcs3 dev_hdd0 directory: ")
        if validate_rpcs3_directory(rpcs3_directory):
            with open(directory_file, "w") as file:
                file.write(rpcs3_directory)
            return rpcs3_directory
        else:
            print("Invalid directory. Please try again.")


def validate_rpcs3_directory(rpcs3_directory):
    game_folder_path = os.path.join(rpcs3_directory, "game")
    blus30463_folder_path = os.path.join(game_folder_path, "BLUS30463")

    if not os.path.exists(blus30463_folder_path):
        print("Rock Band 3 (BLUS30463) not detected in the provided rpcs3 directory. Creating One.")
        os.makedirs(blus30463_folder_path, exist_ok=True)
    
    # This line is adjusted to check the existence of blus30463_folder_path
    return os.path.exists(blus30463_folder_path)

rpcs3_directory = get_rpcs3_directory()

successful_extraction = download_mackiloha()

if successful_extraction:
    if build_patch_ark(False, False, rpcs3_mode=False):
        if is_macos:
            close_rpcs3_process_mac()
        else:
            close_rpcs3_process_windows()

        print("PS3 ARK built successfully!")
        # Copy files from _build/ps3 to rpcs3_directory/game/BLUS30463
        source_dir = "../_build/ps3"
        destination_dir = os.path.join(rpcs3_directory, "game", "BLUS30463")

        # Ensure destination_dir exists before copying
        os.makedirs(destination_dir, exist_ok=True)

        # Copy files
        for root, dirs, files in os.walk(source_dir):
            relative_path = os.path.relpath(root, source_dir)
            for file in files:
                source_file = os.path.join(root, file)
                relative_file_path = os.path.normpath(os.path.join(relative_path, file))
                destination_file = os.path.normpath(os.path.join(destination_dir, relative_file_path))
                
                if is_macos:
                    # Remove leading/trailing quotes and whitespace
                    destination_file = destination_file.strip('"\' ')
                    # Remove escaped backslashes
                    destination_file = destination_file.replace("\\", "")
                    
                os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                shutil.copy2(source_file, destination_file)
                
                # Modify the print statement to format the paths correctly
                print(f"Copied '{source_file}' to '{destination_file}'")

        # Check for rpcs3.exe in the parent folder of rpcs3_directory
        rpcs3_exe_path = os.path.join(os.path.dirname(rpcs3_directory), "rpcs3")
        rpcs3_app_path = "/Applications/RPCS3.app/Contents/MacOS/RPCS3"

        discordrichpresence_path = os.path.join(os.path.dirname(__file__), "discordrichpresence.py")

        suffix = "_rpcs3" if os.path.exists(rpcs3_exe_path) else ""

        # Create the json_path file with the appropriate suffix
        json_path = os.path.join(rpcs3_directory, "game", "BLUS30463", "USRDIR", "discordrp.json")
        with open(f"json_path{suffix}.txt", "w") as file:
            file.write(json_path)

        # Use "python3" on macOS, and "python" on other platforms
        python_command = "python3" if is_macos else "python"

        subprocess.Popen([python_command, discordrichpresence_path, suffix])

        # Run rpcs3 with the appropriate suffix in a detached process
        print("Complete! Launching RPCS3...")
        eboot_bin_path = os.path.join(rpcs3_directory, "game", "BLUS30463", "USRDIR", "eboot.bin")
        eboot_bin_path_escaped = eboot_bin_path.replace(" ", r"\ ")  # Escape the space

        # Use double quotes around the path to handle spaces
        eboot_bin_path_escaped = f'"{eboot_bin_path_escaped}"'

        print(f"Launching RPCS3 with eboot.bin: {eboot_bin_path_escaped}")

        if is_macos:
            run_in_detached_process([rpcs3_app_path, eboot_bin_path])
        else:
            run_in_detached_process([rpcs3_exe_path, eboot_bin_path])

    else:
        print("Error building PS3 ARK. Check your modifications or run git_reset.py to rebase your repo.")