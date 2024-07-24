### README.md

# Prey Mod Creation Tool

## Overview

This tool is designed to help modders of the game Prey (2017) by automating the creation of mods with customizable features. The script modifies specific XML files to adjust recycle values based on user-defined multipliers. Future expansions will include support for generating C# based mods compatible with Chairloader, allowing for easy integration and dynamic configuration within the game.

## Folder Structure

Ensure the following folder structure is present within the `ModdingTemplate` directory:

```
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
├── mod_creator.py
└── run_mod_creator.bat
```

## Supported Features

This modding tool currently supports modifying the following XML attributes:


- RecycleData Table (Means all recycle ways either through RecycleGrenade or RecycleStation

## How to Use

### Running the Script

1. **Run the Script**: Navigate to the `ModdingTemplate` directory and execute the `run_mod_creator.bat` file to start the script using Python 3.12 from the Microsoft Store (dev pack).

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

5. **Zipping and Cleaning Up**:
    - After the patching process is complete, the script will zip the mod folder and save it in the same directory with the mod name.
    - The unzipped mod folder will be deleted after zipping.

6. **Completion**:
    - Once the patching and zipping processes are complete, you will be given the option to create another mod or quit the script.

### Example Run

```
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
├── mod_creator.py
└── run_mod_creator.bat

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

Zipping mod folder...
Mod zipped successfully at <path_to_Patched_folder>.zip
Deleted unzipped mod folder at <path_to_Patched_folder>

Patch created successfully!
Inside the 'MyCustomMod' folder you can see the finished mod. Simply put it into the mods folder and apply the patch in the mod loader.

What would you like to do next? (1: Create another mod, 2: Quit): 
```

## Notes

- **Python 3.12 from Microsoft Store**: Ensure you have Python 3.12 installed from the Microsoft Store (dev pack). The script is compatible with this version.
- **Safety**: The script never modifies the original files in the `Database` folder.
- **Requirements**: The script uses `colorama` for colored terminal output, which you can install by typing `pip install colorama` in the command line.

## Future Development

1. **Maximize Compatibility**:
    - Modify only necessary XML components to ensure maximum compatibility with other mods.
    - Implement functions to only include modified parts in the patch files.
    - Ensure existing modded files are not overwritten unless necessary.

2. **Adding Future Support**:
    - **Expanded Database**: Plan and implement support for an expanded database structure.
    - **Additional Python Scripts**: Modularize the project to allow adding new scripts easily.
    - **Templates**: Provide a library of templates for common modifications.

3. **Generating C# Based Mods**:
    - Plan and implement support for generating C# based mods compatible with Chairloader.
    - Ensure the generated mods are compatible with Chairloader's dynamic configuration and mod loading capabilities.
    - Provide examples and templates for creating C# based mods.

## Documentation

- **Detailed Instructions**: Provide step-by-step instructions for setting up and using the project.
- **Examples**: Include examples for each type of modification and integration.
- **Comments**: Ensure all scripts and templates are thoroughly commented.
- **ReadMe**: Update the README.md file with the latest information and usage instructions.

## Testing

- **Compatibility Testing**: Test the mod with other popular mods to ensure compatibility.
- **Functionality Testing**: Test each new feature and modification type to ensure they work as expected.
- **Performance Testing**: Monitor and optimize the performance of the mod, especially when multiple mods are applied.

## Future Ideas

- **Community Contributions**: Open the project for community contributions and feedback.
- **Automation**: Develop scripts to automate repetitive tasks and testing.
- **UI Improvements**: Enhance the user interface for better usability and accessibility.

By following the above instructions, you should be able to create and customize mods for Prey (2017) using Python 3.12 from the Microsoft Store (dev pack).
If there are any Question don't hesitate to join the Prey Modding discord or start a conversation on Github.
