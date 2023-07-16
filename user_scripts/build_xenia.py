import sys
import subprocess
import os

# List of required packages
required_packages = ["psutil"]

# Check if each package is installed, and if not, install it
for package in required_packages:
    try:
        import psutil
    except ImportError:
        print(f"{package} not found. Installing...")
        subprocess.check_call(["pip", "install", package])

def close_xenia_process():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'xenia_canary.exe':
            print(f"Terminating xenia_canary.exe (PID: {process.info['pid']})")
            process.terminate()
            process.wait()  # Wait for the process to terminate
            break

sys.path.append("../dependencies/dev_scripts")

from download_mackiloha import download_mackiloha
from download_xenia import setup_xenia
close_xenia_process()
from build_ark import build_patch_ark



# Download and extract Mackiloha-suite-archive.zip
if not download_mackiloha():
    print("Failed to download and extract Mackiloha-suite-archive.zip. Exiting.")
    sys.exit(1)

if build_patch_ark(True, rpcs3_mode=False):
    print("Xbox ARK built successfully.")
    print("Checking for updates to Xenia Canary")
    # Get the full path to the build folder
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    build_folder = os.path.join(current_script_directory, "..", "_build", "xbox")
    discordrichpresence_path = os.path.join(os.path.dirname(__file__), "discordrichpresence.py")
    # Create json_path_xenia.txt file
    json_path = os.path.join(build_folder, "discordrp.json")
    with open("json_path_xenia.txt", "w") as file:
        file.write(json_path)
    setup_xenia()
    # Now run discordrichpresence.py with _xenia argument
    subprocess.Popen(["python", discordrichpresence_path, "_xenia"])
    # Run xenia with _xenia argument
    cmd_xenia = "_xenia\\xenia_canary.exe _build\\xbox\\default.xex"
    subprocess.run(cmd_xenia, shell=True, cwd="..")
else:
    print("Error building Xbox ARK. Check your modifications or run git_reset.py to rebase your repo.")
