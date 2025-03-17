from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time as NISHA



def mute_system(mute=True):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    volume.SetMute(int(mute), None)  # Corrected: Added 'None' as the second argument

# Mute System
mute_system(True)
print("Unmuting.....")

NISHA.sleep(3)

# Unmute System (Uncomment to test)
mute_system(False)
