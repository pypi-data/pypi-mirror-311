"""
File: pytreebuilder.py
Creation Date: 2024-11-25
Last Update: 2024-11-25
Creator: eis-x
"""

import os
import logging
import argparse

from .utils import name, version

class PyTreeBuilder:
    """
    Class to create a project structure from a description file.

    Attributes:
        tree_file (str): Path to the project structure description file.
    """

    def __init__(self, tree_file):
        """
        Initializes the PyTreeBuilder class with the project structure description file.

        Args:
            tree_file (str): Path to the project structure description file.
        """
        self.tree_file = tree_file
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
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def create_project_structure(self):
        """
        Creates the project structure from a description file.
        """
        try:
            with open(self.tree_file, 'r', encoding='utf-8') as file:
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
                    os.makedirs(path, exist_ok=True)
                    log_message = f"Directory created: {path}"
                    logging.info(log_message)
                    print(log_message)
                else:
                    directory = os.path.dirname(path)
                    if directory:
                        os.makedirs(directory, exist_ok=True)
                    self.create_file(path)
                    log_message = f"File created: {path}"
                    logging.info(log_message)
                    print(log_message)
        except FileNotFoundError:
            error_message = f"File {self.tree_file} not found."
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
    parser = argparse.ArgumentParser(description="Generate a project structure from a tree file")
    parser.add_argument('-t', '--tree-file-path', type=str, required=True, help='Path to the tree file')
    parser.add_argument('-v', '--version', action='version', version=f'{name.title()} {version}', help="Show program's version number and exit")
    args = parser.parse_args()

    PyTreeBuilder(args.tree_file_path).create_project_structure()

if __name__ == '__main__':
    main()
