import time
import os
import ctypes
import subprocess
import sys

# Website to block
WEBSITE = "www.youtube.com"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"
for_time=10

# Function to check if the script has admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to relaunch script as admin
def run_as_admin():
    if is_admin():
        return  # Already running as admin

    print("Requesting Administrator Privileges...")

    # Relaunch the script with admin rights
    script = sys.executable
    params = " ".join(sys.argv)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 1)
    sys.exit()  # Exit the current script

# Function to modify the hosts file
def modify_hosts_file(block=True):
    try:
        with open(HOSTS_PATH, "r+") as file:
            content = file.readlines()
            file.seek(0)
            
            # Remove existing entries
            for line in content:
                if WEBSITE not in line:
                    file.write(line)

            # Add block entry if needed
            if block:
                file.write(f"{REDIRECT_IP} {WEBSITE}\n")
            
            file.truncate()
        
        action = "blocked" if block else "unblocked"
        print(f"Hosts file updated: {WEBSITE} {action}.")
    except Exception as e:
        print(f"Error modifying hosts file: {e}")

# Function to modify Windows Firewall
def modify_firewall(block=True):
    rule_name = "Block YouTube"
    
    if block:
        command = f'netsh advfirewall firewall add rule name="{rule_name}" dir=out action=block remoteip=172.217.0.0/16 enable=yes'
    else:
        command = f'netsh advfirewall firewall delete rule name="{rule_name}"'
    
    try:
        subprocess.run(command, shell=True, check=True)
        action = "blocked" if block else "unblocked"
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
        print(f"NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA\nFirewall updated: {WEBSITE} {action}. For {for_time} secounds")
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
        print("NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA NISHA")
    except Exception as e:
        print(f"Error modifying firewall: {e}")

# Main function to block and unblock after 1 hour
def block_website_for_an_hour():
    if not is_admin():
        run_as_admin()

    print(f"Blocking {WEBSITE} for {for_time} seconds")

    # Block website
    modify_hosts_file(block=True)
    modify_firewall(block=True)

    # Wait for 1 hour
    time.sleep(for_time)

    # Unblock website
    modify_hosts_file(block=False)
    modify_firewall(block=False)

    print(f"✅ {WEBSITE} has been unblocked after 1 hour.")

# Run the function
if __name__ == "__main__":
    block_website_for_an_hour()
