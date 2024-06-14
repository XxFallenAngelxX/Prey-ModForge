import os
import shutil
import xml.etree.ElementTree as ET
from colorama import init, Fore, Style

# Initialize colorama
init()

# Define paths
DATABASE_FOLDER = os.path.join(os.path.dirname(__file__), 'Database')
MODS_FOLDER = os.path.join(os.path.dirname(__file__), 'Patched')

# Define files to modify for Recycle Amount
FILES_TO_MODIFY_RECYCLE = [
    r'Libs/EntityArchetypes/ArkPhysicsProps.xml',
    r'Libs/EntityArchetypes/ArkHumans.xml',
    r'Libs/EntityArchetypes/ArkRobots.xml',
    r'Libs/EntityArchetypes/ArkGameplayArchitecture.xml',
    r'Libs/EntityArchetypes/ArkInteractiveProps.xml',
    r'Libs/EntityArchetypes/ArkLights.xml',
    r'Libs/EntityArchetypes/ArkNpcs.xml',
    r'Libs/EntityArchetypes/ArkPickups.xml',
    r'Libs/EntityArchetypes/arkprojectiles.xml'
]

def display_multiplier_menu():
    print(Fore.CYAN + "\nSelect the multiplier for the recycle values:" + Style.RESET_ALL)
    print("1. 1.5x")
    print("2. 2x")
    print("3. 3x")
    print("4. 5x")
    print("5. 20x")
    
    while True:
        try:
            choice = int(input(Fore.GREEN + "Enter your choice (1-5): " + Style.RESET_ALL))
            if 1 <= choice <= 5:
                multipliers = {1: 1.5, 2: 2, 3: 3, 4: 5, 5: 20}
                return multipliers[choice]
            else:
                print(Fore.RED + "Invalid choice. Please enter a number between 1 and 5." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number between 1 and 5." + Style.RESET_ALL)

def modify_xml_file(file_path, multiplier):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for recycle_data in root.findall(".//RecycleData"):
            for attribute in ["exotic", "mineral", "organic", "synthetic"]:
                if recycle_data.attrib.get(attribute):
                    try:
                        value = float(recycle_data.attrib[attribute])
                        new_value = value * multiplier
                        recycle_data.set(attribute, str(new_value))
                    except ValueError:
                        print(Fore.YELLOW + f"Skipping non-numeric value for {attribute} in {file_path}" + Style.RESET_ALL)
        
        tree.write(file_path)
    except ET.ParseError as e:
        print(Fore.RED + f"Failed to parse {file_path}: {e}" + Style.RESET_ALL)

def create_mod_info(mod_name, mod_root_folder):
    mod_info_content = f"""<?xml version="1.0"?>
<Mod
    modName="{mod_name}"
    displayName="{mod_name}"
    version="1.0"
    author="Mod Author"
    dllName=""
    hasXML="true"
    hasLevelXML="false"
    enableShaderCompiler="false" />
"""
    mod_info_path = os.path.join(mod_root_folder, 'ModInfo.xml')
    if not os.path.exists(mod_info_path):
        with open(mod_info_path, 'w') as mod_info_file:
            mod_info_file.write(mod_info_content)
        print(Fore.GREEN + f"ModInfo.xml created at {mod_info_path}" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + f"ModInfo.xml already exists at {mod_info_path}, skipping creation." + Style.RESET_ALL)

def main():
    while True:
        print(Fore.CYAN + "Prey Modding Script" + Style.RESET_ALL)
        print(Fore.CYAN + "===================" + Style.RESET_ALL)
        print(Fore.YELLOW + "This script modifies specific XML files in the Prey 2017 game.")
        print("Ensure the following folder structure is in Database:")

        print(Fore.MAGENTA + "\nModdingTemplate")
        print("├── Database")
        print("│   └── Libs")
        print("│       └── EntityArchetypes")
        print("│           ├── arkrobots.xml")
        print("│           ├── arkprojectiles.xml")
        print("│           ├── ArkPickups.xml")
        print("│           ├── ArkPhysicsProps.xml")
        print("│           ├── ArkNpcs.xml")
        print("│           ├── ArkLights.xml")
        print("│           ├── ArkInteractiveProps.xml")
        print("│           ├── ArkHumans.xml")
        print("│           └── ArkGameplayArchitecture.xml")
        print("├── Patched")
        print("├── Prey-ModForge.py")
        print("└── Run-Prey-ModForge.bat" + Style.RESET_ALL)
        
        print(Fore.YELLOW + "\nSupports Currently:" + Style.RESET_ALL)
        print(Fore.YELLOW + " - RecycleData" + Style.RESET_ALL)
        
        print(Fore.YELLOW + "\nThe modified files will be saved in the 'Patched' folder, preserving the folder structure.")
        print("Please refer to README.md for detailed instructions.\n" + Style.RESET_ALL)

        if not os.path.exists(DATABASE_FOLDER):
            print(Fore.RED + f"Database folder not found at {DATABASE_FOLDER}" + Style.RESET_ALL)
            return

        mod_name = input(Fore.GREEN + "Enter the name for your mod: " + Style.RESET_ALL)
        mod_root_folder = os.path.join(MODS_FOLDER, mod_name)
        patched_folder = os.path.join(mod_root_folder, 'Data')

        if os.path.exists(mod_root_folder):
            choice = input(Fore.YELLOW + f"The folder {mod_root_folder} already exists. Do you want to replace it? (y/n): " + Style.RESET_ALL)
            if choice.lower() == 'n':
                print(Fore.RED + "Operation aborted by the user." + Style.RESET_ALL)
                return
            elif choice.lower() == 'y':
                shutil.rmtree(mod_root_folder)
                print(Fore.GREEN + f"Replaced existing folder at {mod_root_folder}" + Style.RESET_ALL)

        os.makedirs(patched_folder, exist_ok=True)
        print(Fore.GREEN + f"Created Patched folder at {patched_folder}" + Style.RESET_ALL)

        multiplier = display_multiplier_menu()

        for file_name in FILES_TO_MODIFY_RECYCLE:
            file_path_db = os.path.join(DATABASE_FOLDER, file_name)
            file_path_patched = os.path.join(patched_folder, file_name)

            if os.path.exists(file_path_db):
                # Create directories if they don't exist
                os.makedirs(os.path.dirname(file_path_patched), exist_ok=True)

                # Copy the original file to patched folder
                shutil.copyfile(file_path_db, file_path_patched)

                # Modify the copied XML file
                modify_xml_file(file_path_patched, multiplier)

                print(Fore.GREEN + f"Patched file saved to {file_path_patched}" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"File {file_path_db} does not exist in the database folder." + Style.RESET_ALL)

        create_mod_info(mod_name, mod_root_folder)

        print(Fore.CYAN + "\nPatch created successfully!" + Style.RESET_ALL)
        print(Fore.CYAN + f"Inside the '{mod_name}' folder you can see the finished mod. Simply put it into the mods folder and apply the patch in the mod loader." + Style.RESET_ALL)

        next_action = input(Fore.CYAN + "\nWhat would you like to do next? (1: Create another mod, 2: Quit): " + Style.RESET_ALL)
        if next_action == '2':
            print(Fore.CYAN + "Quitting the script. Goodbye!" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()