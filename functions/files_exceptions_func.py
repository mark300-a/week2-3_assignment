import json
from pathlib import Path
import shutil

def load_primary_config():
    # Path to the primary configuration file
    primary_config_path = Path("text_files/primary_config.json")

    try:
        # Try to load data from the primary configuration file
        with open(primary_config_path, "r") as json_obj:
            primary_config = json.load(json_obj)
    except FileNotFoundError:
        # If the file doesn't exist, create it with default values
        primary_config = {"Safe Mode": "On", "Memory": "32MB", "Error Log": "logs/errors.log"}
        save_primary_config(primary_config)

    return primary_config

def save_primary_config(primary_config):
    # Path to the primary configuration file
    primary_config_path = Path("text_files/primary_config.json")

    # Save the primary configuration to the file using json.dumps()
    with open(primary_config_path, "w") as json_obj:
        json.dump(primary_config, json_obj, indent=2)

def load_server_configs():
    server_configs_path = Path("text_files/server_configs.json")

    if not server_configs_path.exists():
        # Create an empty configuration file
        save_server_configs([])
        return []

    try:
        with open(server_configs_path, "r") as json_obj:
            server_configs = json.load(json_obj)
    except json.decoder.JSONDecodeError:
        # Handle the case where the file contains invalid JSON
        print("Error: Invalid JSON in server_configs.json. Creating a new file.")
        save_server_configs([])
        return []

    return server_configs


    return server_configs

def save_server_configs(server_configs):
    # Paths to the server configurations file and backup file
    server_configs_path = Path("text_files/server_configs.json")
    backup_path = Path("text_files/server_configs_backup.json")

    # Save the server configurations to the file using json.dumps()
    with open(server_configs_path, "w") as json_obj:
        json.dump(server_configs, json_obj, indent=2)

    # Create a backup of the server_configs.json file
    shutil.copy(server_configs_path, backup_path)

def add_server(primary_config):
    # Create a new server configuration using the primary config as a base
    new_server = primary_config.copy()

    print("\nAdding a new server:")
    for key, value in primary_config.items():
        # Ask the user if they want to modify each value
        modify_value = input(f"Do you want to modify the value for {key}? (yes/no): ").lower()
        if modify_value == 'yes':
            # Get a new value from the user or use the existing value
            new_value = input(f"Enter the new value for {key} [{value}]: ").strip()
            new_server[key] = new_value if new_value else value

    # Load existing server configurations, add the new server, and save
    server_configs = load_server_configs()
    server_configs.append(new_server)
    save_server_configs(server_configs)

    print("New server added successfully.")

def modify_server(server_configs):
    print("\nModifying the configuration of an existing server:")
    display_server_list(server_configs)

    # Get a valid index for the server to modify
    server_index = get_valid_server_index(server_configs)
    selected_server = server_configs[server_index]

    print(f"Selected Server Configuration: {selected_server}")
    
    while True:
        # Ask the user which key they'd like to change
        key_to_modify = input("Enter the key you'd like to change (type 'exit' to stop): ").strip()
        if key_to_modify.lower() == 'exit':
            break

        if key_to_modify not in selected_server:
            # Check if the key exists in the selected server
            print(f"Key '{key_to_modify}' does not exist. Please enter a valid key.")
            continue

        # Ask the user for a new value for the selected key
        new_value = input(f"Enter the new value for {key_to_modify} [{selected_server[key_to_modify]}]: ").strip()
        selected_server[key_to_modify] = new_value if new_value else selected_server[key_to_modify]

    # Save the modified server configurations
    save_server_configs(server_configs)
    print("Server configuration modified successfully.")

def delete_server(server_configs):
    print("\nDeleting an existing server:")
    display_server_list(server_configs)

    # Get a valid index for the server to delete
    server_index = get_valid_server_index(server_configs)
    deleted_server = server_configs.pop(server_index)

    # Save the modified server configurations
    save_server_configs(server_configs)
    print(f"Server configuration deleted successfully: {deleted_server}")

def modify_primary_config(primary_config):
    print("\nModifying the primary configuration:")
    print(f"Current Primary Configuration: {primary_config}")
    
    while True:
        # Ask the user which key they'd like to change
        key_to_modify = input("Enter the key you'd like to change (type 'exit' to stop): ").strip()
        if key_to_modify.lower() == 'exit':
            break

        if key_to_modify not in primary_config:
            # Check if the key exists in the primary config
            print(f"Key '{key_to_modify}' does not exist. Please enter a valid key.")
            continue

        # Ask the user for a new value for the selected key
        new_value = input(f"Enter the new value for {key_to_modify} [{primary_config[key_to_modify]}]: ").strip()
        primary_config[key_to_modify] = new_value if new_value else primary_config[key_to_modify]

    # Save the modified primary configuration
    save_primary_config(primary_config)
    print("Primary configuration modified successfully.")

def display_server_list(server_configs):
    print("\nServer Configurations:")
    for i in range(len(server_configs)):
        print(f"{i + 1}. {server_configs[i]}")

def get_valid_server_index(server_configs):
    while True:
        try:
            # Ask the user for the index of the server they want to modify
            index = int(input("Enter the index of the server you want to modify: ")) - 1
            if 0 <= index < len(server_configs):
                return index
            else:
                print("Invalid index. Please enter a valid index.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

