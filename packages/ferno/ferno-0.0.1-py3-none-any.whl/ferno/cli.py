import argparse
import os

def create_new_app(app_name: str):
    """
    Creates a new folder with a `main.py` file for the app.
    """
    if not app_name.isidentifier():
        print(f"Error: '{app_name}' is not a valid Python identifier.")
        return

    # Ensure the directory does not already exist
    if os.path.exists(app_name):
        print(f"Error: Directory '{app_name}' already exists.")
        return

    # Create the new app directory and `main.py`
    os.makedirs(app_name)
    main_file_path = os.path.join(app_name, "main.py")
    with open(main_file_path, "w") as f:
        f.write('print("hello ferno")\n')

    print(f"Successfully created new app: {app_name}")


def main():
    parser = argparse.ArgumentParser(description="Ferno Framework CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: new
    new_parser = subparsers.add_parser("new", help="Create a new app")
    new_parser.add_argument("app_name", type=str, help="Name of the new app directory")

    args = parser.parse_args()

    if args.command == "new":
        create_new_app(args.app_name)
