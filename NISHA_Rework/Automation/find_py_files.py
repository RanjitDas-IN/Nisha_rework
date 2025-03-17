import os
import time
import subprocess
import fnmatch

# 🔍 Function to search for files
def find_files(directory, pattern="*.*"):
    """Search for specific files in a directory and return the matches."""
    matches = []
    for root, _, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            matches.append(os.path.join(root, filename))
    return matches

def open_file_in_cmd(filepath):
    """Open a file in a separate CMD window and keep it open."""
    try:
        subprocess.Popen(f'start cmd /k "{filepath}"', shell=True)
        print(f"✅ Opened in new CMD: {filepath}")
    except Exception as e:
        print(f"❌ Error opening file: {e}")

# 🎤 Take user input
def manual_file_search():
    """Take user input to search for files."""
    search_term = input("🔎 Enter what files you want to find: ").lower().strip()

    # Determine file type based on user input
    if "python" in search_term:
        file_extension = "*.py"
    elif "text" in search_term:
        file_extension = "*.txt"
    elif "document" in search_term:
        file_extension = "*.docx"
    elif "image" in search_term:
        file_extension = "*.jpg"
    else:
        file_extension = "*.*"  # Search for all files

    search_path = r"E:\Till_ML\PYTHON PROGRAMS     🐍🐍🐍"
    results = find_files(search_path, file_extension)

    if results:
        print("📂 Found these files:")
        for file in results[:5]:  # Show only top 5 results
            print(f" - {file}")
            open_file_in_cmd(file)
            
            
    else:
        print("❌ No files found.")

# 🎯 Run manual file search
manual_file_search()
