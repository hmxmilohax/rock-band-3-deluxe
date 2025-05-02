import os
import fnmatch

# Patterns of macOS hidden files and directories
HIDDEN_PATTERNS = ['.DS_Store', '._*', '.Spotlight-V100', '.Trashes']

def remove_macos_hidden_files(base_path='.'):
    removed_files = []
    for root, dirs, files in os.walk(base_path):
        # Remove unwanted files
        for pattern in HIDDEN_PATTERNS:
            for filename in fnmatch.filter(files, pattern):
                file_path = os.path.join(root, filename)
                try:
                    os.remove(file_path)
                    removed_files.append(file_path)
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")

        # Remove unwanted directories
        for pattern in HIDDEN_PATTERNS:
            for dir_name in fnmatch.filter(dirs, pattern):
                dir_path = os.path.join(root, dir_name)
                try:
                    os.rmdir(dir_path)
                    removed_files.append(dir_path)
                except Exception as e:
                    print(f"Failed to remove {dir_path}: {e}")

    print("Removed the following macOS hidden files/directories:")
    for f in removed_files:
        print(f" - {f}")

if __name__ == '__main__':
    remove_macos_hidden_files()
