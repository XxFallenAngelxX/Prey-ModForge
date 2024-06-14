
# Prey Modding Script

## Overview
This script is designed to help modders of the game Prey (2017) by modifying specific XML files to adjust recycle values. The script creates a new mod with user-specified multipliers for the recycle values and saves the modified files in a new folder, preserving the original database files.

## Folder Structure
Ensure the following folder structure is present within the `ModdingTemplate` directory:

ModdingTemplate
├── Database
│   └── Libs
│       └── EntityArchetypes
│           ├── ArkRobots.xml
│           ├── ArkProjectiles.xml
│           ├── ArkPickups.xml
│           ├── ArkPhysicsProps.xml
│           ├── ArkNpcs.xml
│           ├── ArkLights.xml
│           ├── ArkInteractiveProps.xml
│           ├── ArkHumans.xml
│           └── ArkGameplayArchitecture.xml
├── Patched
├── prey_mod.py
└── run_prey_mod.bat

## Supported Features
Currently, this script supports modifying the following XML attributes:

- RecycleData

## How to Use
1. **Run the Script**: Navigate to the `ModdingTemplate` directory and execute the `run_prey_mod.bat` file to start the script using Python 3.12 from the Microsoft Store (dev pack).

2. **Follow the Prompts**:
    - **Mod Name**: Enter a name for your mod when prompted.
    - **Select Multiplier**: Choose a multiplier for the recycle values from the options provided (1.5x, 2x, 3x, 5x, 20x).

3. **Folder Handling**:
    - If a folder with the specified mod name already exists, you will be asked whether you want to replace it.
    - If you choose to replace it, the existing folder will be deleted, and a new folder will be created with the same name.
    - If you choose not to replace it, the operation will be aborted.

4. **Patched Files**:
    - The script copies the original files from the `Database` folder to the new mod folder under `Patched`, then modifies these copied files.
    - The modified files will be saved in the `Patched` folder, preserving the original structure.

5. **Completion**:
    - Once the patching process is complete, you will be given the option to create another mod or quit the script.


## Example Run

Prey Modding Script

===================

This script modifies specific XML files in the Prey 2017 game.
Ensure the following folder structure is in Database:

ModdingTemplate
├── Database
│   └── Libs
│       └── EntityArchetypes
│           ├── ArkRobots.xml
│           ├── ArkProjectiles.xml
│           ├── ArkPickups.xml
│           ├── ArkPhysicsProps.xml
│           ├── ArkNpcs.xml
│           ├── ArkLights.xml
│           ├── ArkInteractiveProps.xml
│           ├── ArkHumans.xml
│           └── ArkGameplayArchitecture.xml
├── Patched
├── prey_mod.py
└── run_prey_mod.bat

Supports Currently:
 - RecycleData

The modified files will be saved in the 'Patched' folder, preserving the folder structure.

Enter the name for your mod: MyCustomMod
Select the multiplier for the recycle values:
1. 1.5x
2. 2x
3. 3x
4. 5x
5. 20x
Enter your choice (1-5): 2

Created Patched folder at <path_to_Patched_folder>
Patched file saved to <path_to_Patched_folder>/Libs/EntityArchetypes/ArkPhysicsProps.xml
...
ModInfo.xml created at <path_to_Patched_folder>/ModInfo.xml

Patch created successfully!
Inside the 'MyCustomMod' folder you can see the finished mod. Simply put it into the mods folder and apply the patch in the mod loader.

What would you like to do next? (1: Create another mod, 2: Quit): 


## Notes
- **Python 3.12 from Microsoft Store**: Ensure you have Python 3.12 installed from the Microsoft Store (dev pack). The script is compatible with this version.
- **Safety**: The script never modifies the original files in the `Database` folder.
- **Requirements**: The script uses `colorama` for colored terminal output, which you can install by typing `pip install colorama`command in the CMD (win+R to open).

By following the above instructions, you should be able to create and customize mods for Prey (2017) using Python 3.12 from the Microsoft Store (dev pack).

