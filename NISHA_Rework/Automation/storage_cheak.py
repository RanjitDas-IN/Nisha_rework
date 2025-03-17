import psutil

def get_drive_info():
    partitions = psutil.disk_partitions()
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total = usage.total / (1024 ** 3)  # Convert bytes to GB
            free = usage.free / (1024 ** 3)  # Convert bytes to GB
            
            print(f"{partition.device} {free:.1f} GB free of {total:.1f} GB")
        
        except PermissionError:
            continue  # Skip drives that require special permissions

get_drive_info()
