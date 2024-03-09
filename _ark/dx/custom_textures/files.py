import os

# Function to recursively scan folders and create list.txt files
def scan_folder(folder_path):
    # Create a list to store file names
    file_list = []
    # Iterate over each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isdir(file_path):
            # If the file is a directory, recursively scan it
            scan_folder(file_path)
        elif file_name.endswith(".png"):
            # Add the file name to the list, encapsulated in single quotes
            file_list.append(f"'{os.path.splitext(file_name)[0]}'")
    
    if file_list:
        # Sort the list of file names alphabetically
        file_list.sort()
        # Write the list of file names to a txt file
        with open(os.path.join(folder_path, "_list.dta"), "w") as file:
            file.write("\n".join(file_list))

# Get the current directory
current_dir = os.getcwd()

# Recursively scan folders starting from the current directory
scan_folder(current_dir)
