"""
File: pytreebuilder.py
Creation Date: 2024-11-25
Last Update: 2024-11-25
Creator: eis-x
"""

import os
import logging
import argparse

class PyTreeBuilder:
    """
    Class to create a project structure from a description file.

    Attributes:
        tree_file_path (str): Path to the project structure description file.
        update_mode (bool): Flag to indicate if the script should run in update mode.
    """

    def __init__(self, tree_file_path, update_mode=False):
        """
        Initializes the PyTreeBuilder class with the project structure description file.

        Args:
            tree_file_path (str): Path to the project structure description file.
            update_mode (bool): Flag to indicate if the script should run in update mode.
        """
        self.tree_file_path = tree_file_path
        self.update_mode = update_mode
        self.setup_logging()

    def setup_logging(self):
        """
        Configures the logging system.
        """
        if not os.path.exists('logs'):
            os.makedirs('logs')

        logging.basicConfig(filename='logs/pytreebuilder.log', level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s', encoding='utf-8')

        logging.info("Starting PyTreeBuilder")

    def create_file(self, file_path, content=""):
        """
        Creates a file with the specified content.

        Args:
            file_path (str): Path to the file to be created.
            content (str): Content to write to the file.
        """
        if os.path.exists(file_path):
            if self.update_mode:
                logging.info(f"File {file_path} already exists. Skipping in update mode.")
                print(f"Skipping existing file: {file_path}")
                return
            else:
                overwrite = input(f"File {file_path} already exists. Overwrite? (y/n): ")
                logging.info(f"User response for overwriting file {file_path}: {overwrite}")
                if overwrite.lower() != 'y':
                    print(f"Skipping file: {file_path}")
                    logging.info(f"Skipping file: {file_path}")
                    return
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        logging.info(f"File created: {file_path}")
        print(f"File created: {file_path}")

    def create_project_structure(self):
        """
        Creates the project structure from a description file.
        """
        try:
            with open(self.tree_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            current_path = []
            for line in lines:
                line = line.rstrip()
                depth = line.count('│') + line.count('├') + line.count('└') + line.count('    ')
                name = line.split(' ')[-1]

                # Update the current path based on the depth
                if depth < len(current_path):
                    current_path = current_path[:depth]
                current_path.append(name)

                path = os.path.join(*current_path)
                if name.endswith('/'):
                    if os.path.exists(path):
                        if self.update_mode:
                            logging.info(f"Directory {path} already exists. Skipping in update mode.")
                            print(f"Skipping existing directory: {path}")
                            continue
                        else:
                            overwrite = input(f"Directory {path} already exists. Overwrite? (y/n): ")
                            logging.info(f"User response for overwriting directory {path}: {overwrite}")
                            if overwrite.lower() != 'y':
                                print(f"Skipping directory: {path}")
                                logging.info(f"Skipping directory: {path}")
                                continue
                    os.makedirs(path, exist_ok=True)
                    log_message = f"Directory created: {path}"
                    logging.info(log_message)
                    print(log_message)
                else:
                    directory = os.path.dirname(path)
                    if directory:
                        os.makedirs(directory, exist_ok=True)
                    self.create_file(path)
        except FileNotFoundError:
            error_message = f"File {self.tree_file_path} not found."
            logging.error(error_message)
            print(error_message)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            logging.error(error_message)
            print(error_message)
        finally:
            logging.info("PyTreeBuilder execution finished")


def main():
    """
    Main entry point of the script.
    """
    from utils import name, version
    parser = argparse.ArgumentParser(description="Generate a project structure from a tree file")
    parser.add_argument('-t', '--tree-file-path', type=str, required=True, help='Path to the tree file')
    parser.add_argument('-u', '--update', action='store_true', help='Run in update mode')
    parser.add_argument('-v', '--version', action='version', version=f'{name.title()} {version}', help="Show program's version number and exit")
    args = parser.parse_args()

    # Check if the root directory of the project structure already exists
    with open(args.tree_file_path, 'r', encoding='utf-8') as file:
        first_line = file.readline().rstrip()
    root_dir = first_line.split(' ')[-1]

    if os.path.exists(root_dir) and not args.update:
        proceed = input(f"Project structure {root_dir} already exists. Continue? (y/n): ")
        logging.info(f"User response for continuing with existing project structure {root_dir}: {proceed}")
        if proceed.lower() != 'y':
            print("Operation cancelled.")
            logging.info("Operation cancelled by user.")
            return

    PyTreeBuilder(args.tree_file_path, update_mode=args.update).create_project_structure()

if __name__ == '__main__':
    main()