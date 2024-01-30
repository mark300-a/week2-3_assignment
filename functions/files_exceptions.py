import json
from pathlib import Path
import shutil

def load_primary_config():
    primary_config_path = Path("text_files/primary_config.json")

    try:
        with open(primary_config_path, "r") as json_obj:
            primary_config = json.load(json_obj)
    except FileNotFoundError:
        primary_config = {"Safe Mode": "On", "Memory": "32MB", "Error Log": "logs/errors.log"}
        save_primary_config(primary_config)

    return primary_config

def save_primary_config(primary_config):
    primary_config_path = Path("text_files/primary_config.json")

    with open(primary_config_path, "w") as json_obj:
        json.dump(primary_config, json_obj, indent=2)

def load_server_configs():
    server_configs_path = Path("text_files/server_configs.json")

    try:
        with open(server_configs_path, "r") as json_obj:
            server_configs = json.load(json_obj)
    except FileNotFoundError:
        server_configs = []

    return server_configs

def save_server_configs(server_configs):
    server_configs_path = Path("text_files/server_configs.json")

    # Create a backup before overwriting
    backup_path = server_configs_path.with_suffix('.bak')
    shutil.copy(server_configs_path, backup_path)

    with open(server_configs_path, "w") as json_obj:
        json.dump(server_configs, json_obj, indent=2)

def add_server(primary_config):
    new_server = primary_config.copy()

    print("\nAdding a new server:")
    for key, value in primary_config.items():
        modify_value = input(f"Do you want to modify the value for {key}? (yes/no): ").lower()
        if modify_value == 'yes':
            new_value = input(f"Enter the new value for {key} [{value}]: ").strip()
            new_server[key] = new_value if new_value else value

    server_configs = load_server_configs()
    server_configs.append(new_server)
    save_server_configs(server_configs)

    print("New server added successfully.")

def modify_server(server_configs):
    print("\nModifying the configuration of an existing server:")
    display_server_list(server_configs)
    
    server_index = get_valid_server_index(server_configs)
    selected_server = server_configs[server_index]

    print(f"Selected Server Configuration: {selected_server}")
    
    while True:
        key_to_modify = input("Enter the key you'd like to change (type 'exit' to stop): ").strip()
        if key_to_modify.lower() == 'exit':
            break

        if key_to_modify not in selected_server:
            print(f"Key '{key_to_modify}' does not exist. Please enter a valid key.")
            continue

        new_value = input(f"Enter the new value for {key_to_modify} [{selected_server[key_to_modify]}]: ").strip()
        selected_server[key_to_modify] = new_value if new_value else selected_server[key_to_modify]

    save_server_configs(server_configs)
    print("Server configuration modified successfully.")

def delete_server(server_configs):
    print("\nDeleting an existing server:")
    display_server_list(server_configs)

    server_index = get_valid_server_index(server_configs)
    deleted_server = server_configs.pop(server_index)

    save_server_configs(server_configs)
    print(f"Server configuration deleted successfully: {deleted_server}")

def modify_primary_config(primary_config):
    print("\nModifying the primary configuration:")
    print(f"Current Primary Configuration: {primary_config}")
    
    while True:
        key_to_modify = input("Enter the key you'd like to change (type 'exit' to stop): ").strip()
        if key_to_modify.lower() == 'exit':
            break

        if key_to_modify not in primary_config:
            print(f"Key '{key_to_modify}' does not exist. Please enter a valid key.")
            continue

        new_value = input(f"Enter the new value for {key_to_modify} [{primary_config[key_to_modify]}]: ").strip()
        primary_config[key_to_modify] = new_value if new_value else primary_config[key_to_modify]

    save_primary_config(primary_config)
    print("Primary configuration modified successfully.")

def display_server_list(server_configs):
    print("\nServer Configurations:")
    for i in range(len(server_configs)):
        print(f"{i + 1}. {server_configs[i]}")

def get_valid_server_index(server_configs):
    while True:
        try:
            index = int(input("Enter the index of the server you want to modify: ")) - 1
            if 0 <= index < len(server_configs):
                return index
            else:
                print("Invalid index. Please enter a valid index.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
