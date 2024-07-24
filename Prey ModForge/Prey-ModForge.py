import os
import sys
import subprocess
import shutil
import xml.etree.ElementTree as ET
import logging
import msvcrt
import time
from collections import defaultdict
from colorama import init, Fore, Style
import zipfile

# Function to check and install colorama
def install_colorama():
    try:
        import colorama
    except ImportError:
        print("colorama not found. Installing colorama...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
        import colorama

# Ensure Python version is 3.12
if not (sys.version_info.major == 3 and sys.version_info.minor == 12):
    print(f"Python 3.12 is required. Current version is {sys.version}")
    sys.exit(1)

# Initialize colorama
install_colorama()
init(autoreset=True)

# Setup logging
LOGS_FOLDER = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOGS_FOLDER, exist_ok=True)
logging.basicConfig(filename=os.path.join(LOGS_FOLDER, 'RecycleLog.log'), level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Script started for RecycleTable feature")

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

# Function to display the multiplier menu and return the selected multiplier
def display_multiplier_menu():
    print(Fore.CYAN + "\nSelect the multiplier for the recycle values:" + Style.RESET_ALL)
    print("1. 1.5x")
    print("2. 2x")
    print("3. 3x")
    print("4. 5x")
    print("5. 20x")
    
    while True:
        try:
            choice = msvcrt.getch().decode('utf-8')
            if choice in '12345':
                multipliers = {'1': 1.5, '2': 2, '3': 3, '4': 5, '5': 20}
                logging.info(f"Multiplier selected: {multipliers[choice]}")
                print(f"\nSelected multiplier: {multipliers[choice]}")
                return multipliers[choice]
            else:
                print(Fore.RED + "Invalid choice. Please enter a number between 1 and 5." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number between 1 and 5." + Style.RESET_ALL)

# Function to modify XML files based on the selected multiplier
def modify_xml_file(file_path, multiplier, changes_summary, error_summary):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Iterate over all RecycleData elements and modify their attributes
        for recycle_data in root.findall(".//RecycleData"):
            for attribute in ["exotic", "mineral", "organic", "synthetic"]:
                if recycle_data.attrib.get(attribute):
                    try:
                        value = float(recycle_data.attrib[attribute])
                        new_value = value * multiplier
                        recycle_data.set(attribute, str(new_value))
                        changes_summary[attribute]['modified'] += 1
                    except ValueError:
                        error_summary[attribute] += 1
                        logging.warning(f"Skipping non-numeric value for {attribute} in {file_path}")
                        print(Fore.YELLOW + f"Skipping non-numeric value for {attribute} in {file_path}" + Style.RESET_ALL)
        
        tree.write(file_path)
        logging.info(f"File saved: {file_path}")
    except ET.ParseError as e:
        logging.error(f"Failed to parse {file_path}: {e}")
        print(Fore.RED + f"Failed to parse {file_path}: {e}" + Style.RESET_ALL)
        error_summary['parse_errors'] += 1

# Function to create ModInfo.xml file
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
        logging.info(f"ModInfo.xml created at {mod_info_path}")
        print(Fore.GREEN + f"ModInfo.xml created at {mod_info_path}" + Style.RESET_ALL)
    else:
        logging.warning(f"ModInfo.xml already exists at {mod_info_path}, skipping creation.")
        print(Fore.YELLOW + f"ModInfo.xml already exists at {mod_info_path}, skipping creation." + Style.RESET_ALL)

# Function to zip the mod folder
def zip_mod_folder(mod_name, mod_root_folder):
    zip_filename = os.path.join(MODS_FOLDER, f"{mod_name}.zip")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(mod_root_folder):
            for file in files:
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                           os.path.join(mod_root_folder, '..')))
    logging.info(f"Mod zipped successfully at {zip_filename}")
    print(Fore.GREEN + f"Mod zipped successfully at {zip_filename}" + Style.RESET_ALL)

# Main function
def main():
    while True:
        print(Fore.CYAN + "Prey Modding Script" + Style.RESET_ALL)
        print(Fore.CYAN + "===================" + Style.RESET_ALL)
        print(Fore.YELLOW + "This script modifies specific XML files in the Prey 2017 game.")
        print("Ensure the following folder structure is in Database:")

        print(Fore.MAGENTA + "\nModdingTemplate")
        print("|-- Database")
        print("|   |-- Libs")
        print("|       |-- EntityArchetypes")
        print("|           |-- arkrobots.xml")
        print("|           |-- arkprojectiles.xml")
        print("|           |-- ArkPickups.xml")
        print("|           |-- ArkPhysicsProps.xml")
        print("|           |-- ArkNpcs.xml")
        print("|           |-- ArkLights.xml")
        print("|           |-- ArkInteractiveProps.xml")
        print("|           |-- ArkHumans.xml")
        print("|           |-- ArkGameplayArchitecture.xml")
        print("|-- Patched")
        print("|-- mod_creator.py")
        print("|-- run_mod_creator.bat" + Style.RESET_ALL)
        
        print(Fore.YELLOW + "\nSupports Currently:" + Style.RESET_ALL)
        print(Fore.YELLOW + " - RecycleData" + Style.RESET_ALL)
        
        print(Fore.YELLOW + "\nThe modified files will be saved in the 'Patched' folder, preserving the folder structure.")
        print("Please refer to README.md for detailed instructions.\n" + Style.RESET_ALL)

        # Check if Database folder exists
        if not os.path.exists(DATABASE_FOLDER):
            logging.error(f"Database folder not found at {DATABASE_FOLDER}")
            print(Fore.RED + f"Database folder not found at {DATABASE_FOLDER}" + Style.RESET_ALL)
            return

        # Get mod name from user
        mod_name = input(Fore.GREEN + "Enter the name for your mod: " + Style.RESET_ALL)
        mod_root_folder = os.path.join(MODS_FOLDER, mod_name)
        patched_folder = os.path.join(mod_root_folder, 'Data')

        # Handle existing mod folder
        if os.path.exists(mod_root_folder):
            choice = input(Fore.YELLOW + f"The folder {mod_root_folder} already exists. Do you want to replace it? (y/n): " + Style.RESET_ALL)
            if choice.lower() == 'n':
                logging.info("Operation aborted by the user.")
                print(Fore.RED + "Operation aborted by the user." + Style.RESET_ALL)
                return
            elif choice.lower() == 'y':
                shutil.rmtree(mod_root_folder)
                logging.info(f"Replaced existing folder at {mod_root_folder}")
                print(Fore.GREEN + f"Replaced existing folder at {mod_root_folder}" + Style.RESET_ALL)

        # Create patched folder
        os.makedirs(patched_folder, exist_ok=True)
        logging.info(f"Created Patched folder at {patched_folder}")
        print(Fore.GREEN + f"Created Patched folder at {patched_folder}" + Style.RESET_ALL)

        # Display multiplier menu and get selected multiplier
        multiplier = display_multiplier_menu()

        # Dictionaries to summarize changes and errors
        changes_summary = defaultdict(lambda: defaultdict(int))
        error_summary = defaultdict(int)

        # Modify files and update summary
        for file_name in FILES_TO_MODIFY_RECYCLE:
            file_path_db = os.path.join(DATABASE_FOLDER, file_name)
            file_path_patched = os.path.join(patched_folder, file_name)

            if os.path.exists(file_path_db):
                # Create directories if they don't exist
                os.makedirs(os.path.dirname(file_path_patched), exist_ok=True)

                # Copy the original file to patched folder
                shutil.copyfile(file_path_db, file_path_patched)

                # Modify the copied XML file
                modify_xml_file(file_path_patched, multiplier, changes_summary, error_summary)

        # Create ModInfo.xml file
        create_mod_info(mod_name, mod_root_folder)

        logging.info("Patch created successfully")
        print(Fore.CYAN + "\nPatch created successfully!" + Style.RESET_ALL)
        print(Fore.CYAN + f"Inside the '{mod_name}' folder you can see the finished mod. Simply put it into the mods folder and apply the patch in the mod loader." + Style.RESET_ALL)

        # Zip the mod folder
        print(Fore.CYAN + "\nZipping mod folder..." + Style.RESET_ALL)
        zip_mod_folder(mod_name, mod_root_folder)
        
        # Delete the unzipped mod folder
        shutil.rmtree(mod_root_folder)
        logging.info(f"Deleted unzipped mod folder at {mod_root_folder}")
        print(Fore.CYAN + f"Deleted unzipped mod folder at {mod_root_folder}" + Style.RESET_ALL)

        # Summary of changes
        logging.info("Summary of modifications:")
        for attribute, counts in changes_summary.items():
            logging.info(f"  {attribute.capitalize()} - Modified: {counts['modified']}, Errors: {error_summary[attribute]}")
        
        logging.info(f"Total parse errors: {error_summary['parse_errors']}")

        print(Fore.CYAN + "\nWhat would you like to do next? (1: Create another mod, 2: Quit): " + Style.RESET_ALL)
        next_action = msvcrt.getch().decode('utf-8')
        if next_action == '1':
            continue
        elif next_action == '2':
            logging.info("Quitting the script. Goodbye!")
            print(Fore.CYAN + "Quitting the script. Goodbye!" + Style.RESET_ALL)
            time.sleep(1)  # Wait for 1 second before closing
            return

if __name__ == "__main__":
    main()