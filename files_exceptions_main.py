# Import functions from the files_exceptions_func module
from functions.files_exceptions_func import *

# Load the primary configuration
primary_config = load_primary_config()
# load server configurations
server_configs = load_server_configs()

# Main program loop
while True:
    # Display menu options
    print("\nMenu:")
    print("1. Add a new server")
    print("2. Modify the configuration of an existing server")
    print("3. Delete an existing server")
    print("4. Modify Primary Configuration")
    print("5. Save server configuration data")
    print("6. Exit Program")

    # Get user choice
    choice = input("Enter your choice: ").strip()

    # Process user choice
    if choice == '1':
        # Option to add a new server
        add_server(primary_config)
    elif choice == '2':
        # Option to modify the config of an existing server
        modify_server(server_configs)
    elif choice == '3':
        # delete an existing server
        delete_server(server_configs)
    elif choice == '4':
        # mod primary config
        modify_primary_config(primary_config)
    elif choice == '5':
        # save server config data
        save_server_configs(server_configs)
    elif choice == '6':
        # option to exit
        break
