import os
import time
import shutil

# Folder to monitor (change this as needed)
# FOLDER_PATH = os.path.expanduser(r"C:\Users\ranji\OneDrive\Pictures\Screenshots 1")
To_beDelete_FOLDER_PATH = os.path.expanduser(r"C:\Users\ranji\OneDrive\Pictures\temp")  

def find_and_delete_screenshots(folder):
    """Finds and deletes all screenshot images (PNG, JPG) in the folder."""
    deleted_files = []
    for file in os.listdir(folder):
        if file.lower().endswith((".png", ".jpg", ".jpeg")) and "screenshot" in file.lower():
            file_path = os.path.join(folder, file)
            os.remove(file_path)  # Delete file
            deleted_files.append(file)
    return deleted_files

def monitor_folder(folder):
    """Monitors the folder for new files and notifies when a new file is added."""
    existing_files = set(os.listdir(folder))
    print(f"Monitoring {folder} for new files...")

    while True:
        time.sleep(2)  # Check every 2 seconds
        current_files = set(os.listdir(folder))
        new_files = current_files - existing_files

        if new_files:
            print(f"📂 New file(s) added: {', '.join(new_files)}")
            existing_files = current_files  # Update file list

if __name__ == "__main__":
    if not os.path.exists(To_beDelete_FOLDER_PATH):
        print("Error: Folder does not exist.")
    else:
        deleted = find_and_delete_screenshots(To_beDelete_FOLDER_PATH)
        if deleted:
            print(f"🗑 Deleted screenshots: {', '.join(deleted)}")
        else:
            print("✅ No screenshots found.")

        # Start monitoring the folder for new files
        # monitor_folder(FOLDER_PATH)
