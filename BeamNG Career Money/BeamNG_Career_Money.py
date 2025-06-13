import os
import re
from pathlib import Path
from typing import Optional
import json
import time
import math
from sys import exit

# Global variables

userset = False
input_str = 0
addorsubvalue = "0"
s = addorsubvalue.strip()

# This function find the latest version of BeamNG.drive in the localappdata directory

def latestbngversion(beamng_root: Path) -> Optional[Path]:
    version_dirs = []
    version_pattern = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?$")
    # Regex pattern to match version directories
    # Try loop for safety
    try:
        for child in beamng_root.iterdir():
            if not child.is_dir():
                continue

            match = version_pattern.match(child.name)
            if not match:
                continue

            parts = match.groups(default="0")
            version_tuple = tuple(int(p) for p in parts)
            version_dirs.append((version_tuple, child))
    except FileNotFoundError:
        return None
    except PermissionError:
        return None

    if not version_dirs:
        return None

    latest_version, latest_dir = max(version_dirs, key=lambda x: x[0])
    return latest_dir

# This lists all the saves in the BeamNG.drive directory folder
def list_saves(sav_root: Path) -> Optional[Path]:
    candidates = []
    try:
        for item in sav_root.iterdir():
            if item.is_dir():
                candidates.append((item.name, item))
    except (FileNotFoundError , PermissionError):
        return None

    if not candidates:
        return None
    return candidates

# This function finds the most recent playerAttributes.json file in the users selected save directory

def recent_playattpath(selsaveroot: Path) -> Optional[Path]:
    autosaves = []
    datemod = []
    try:
        for child in selsaveroot.iterdir():
            if not child.is_dir():
                continue
            autosaves.append(child)
    except (FileNotFoundError , PermissionError):
        return None
    if not autosaves:
        return None
    try:
        for autosave in autosaves:
            d8modified = os.path.getmtime(selsaveroot / autosave / "career" / "playerAttributes.json")
            datemod.append((d8modified, autosave))
    except (FileNotFoundError, PermissionError):
        return None
    if not datemod:
        return None
    latest_mod, latest_autosav = max(datemod, key=lambda x: x[0])
    recentplayattpath = selsaveroot / latest_autosav / "career" / "playerAttributes.json"
    return recentplayattpath

# This function takes the current money value and value to be added or subtratced and returns the new value
def updatevalue(base, input_str):
    input_str = str(input_str).strip()

    if input_str.startswith('-'):
        amount = int(input_str[1:])
        return base - amount
    else:
        amount = int(input_str)
        return base + amount


# Main script execution

if __name__ == "__main__":
    # On Windows, better to read from LOCALAPPDATA
    local_appdata = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    beamng_root = local_appdata / "BeamNG.drive"

    latest = latestbngversion(beamng_root)
    print("WARNING! If your BeamNG carrer mode is still open this tool wil not work!")
    time.sleep(2)
    print("continuing...")
    if latest:
        print(f"Latest BeamNG.drive version found!: {latest.name} at {latest}")
    else:
        print("ERR: No BeamNG.Drive versions found -- If your files are in the default directory make a github report!")
        exit()

    sav_root = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))) / "BeamNG.drive" / latest.name / "settings" / "cloud" / "saves"
    saves = list_saves(sav_root)


    print("Saves found!: Please select which save you would like to edit")
    for i, (name, path) in enumerate(saves, start=1):
        print(f"{i}: {name}")
    while True:
        choice = input("Save Number: ").strip()
        if not choice.isdigit():
                print("Invalid input. Please enter a valid number.")
                continue
        actual_input = int(choice) - 1
        if 0 <= actual_input < len(saves):
            selected_save = saves[actual_input][1]
            print(f"Selected save: {saves[actual_input][0]}")
            break
        print("Your input is out of range.")

    selsaveroot = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))) / "BeamNG.drive" / latest.name / "settings" / "cloud" / "saves" / selected_save
    latestautosavpath = recent_playattpath(selsaveroot)
    if not latestautosavpath:
        print("ERR: No autosaves found in the selected save directory. ")
        exit()
    else:
        with open(latestautosavpath, 'r') as file:
            data = json.load(file)
        moneyval = data["money"]["value"]
        print(f"Latest autosave found at: {latestautosavpath}")
        print("")
        print("Would you like to add the default, add or subtract a custom amount, or set ur money value?")
        print("Enter: Adds $1500 (default)")
        print("1: Custom Amount")
        print("2: Set Money Value")
        print(f"Current Value {moneyval}")
        while True:
            userselection = input(">>> ").strip()
            if userselection == "":
                addorsubvalue = 1500
                userset = False
                break

            elif userselection == "1":
                # inner loop just for your custom-amount entry
                while True:
                    entry = input("How much money would you like to add or subtract? ").strip()
                    if entry.lstrip('-').isdigit():
                        addorsubvalue = entry      # keep as string so updatevalue sees the “-”
                        userset = False
                        break
                    print("Invalid number. Try again!")
                break

            elif userselection == "2":
                # inner loop for setting absolute value
                while True:
                    entry = input("What would you like to set career money to? ").strip()
                    if entry.isdigit():
                        addorsubvalue = entry
                        userset = True
                        break
                    print("Invalid number. Try again!")
                break

            else:
                print("Invalid choice — hit Enter, or enter 1 or 2.")
                # loops back to the top of this while True
    if userset == True:
        addorsub = addorsubvalue
        data["money"]["value"] = addorsub
        with open(latestautosavpath, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        addorsub = updatevalue(data["money"]["value"], addorsubvalue)
        data["money"]["value"] = addorsub
        with open(latestautosavpath, 'w') as file:
            json.dump(data, file, indent=4)
    
    print("Checking if the file was updated...")
    time.sleep(.5)
    with open(latestautosavpath, 'r') as file:
        newdata = json.load(file)
        if newdata["money"]["value"] != moneyval:
            print(f"Change Successful! New Money Value: {newdata['money']['value']}")
        else:
            print("ERR: Value was not changed :( Send a report")



    
                    

