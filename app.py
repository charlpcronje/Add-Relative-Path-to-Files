import os
import json
import argparse
import logging

def process_file(file_path, comment_style, project_root, comment_after=None, comment_end=None, logger=None):
    """
    Adds a comment with the relative file path to the beginning of a file,
    immediately after a specified marker (if provided), and logs the action.

    :param file_path: Path of the file to process.
    :param comment_style: Style of the comment to add.
    :param project_root: Root directory of the project for calculating relative paths.
    :param comment_after: Optional marker after which the comment should be added.
    :param comment_end: Optional ending marker for the comment (for block comments).
    :param logger: Logger object for logging actions.
    """
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Construct the comment string
    relative_path = os.path.relpath(file_path, project_root)
    relative_path_comment = f"{comment_style} {relative_path}"
    if comment_end:
        relative_path_comment += f" {comment_end}"

    # Check if the comment already exists in the file
    if any(relative_path_comment in line for line in content):
        if logger:
            logger.info(f"Skipped: Comment already added for {relative_path}")
        return  # Skip this file as the comment already exists

    # Adding the comment based on the conditions
    if comment_after:
        # Search for the specified marker to insert the comment after
        for i, line in enumerate(content):
            if comment_after in line:
                # Check if the next line already starts with the comment style
                if i + 1 < len(content) and content[i + 1].strip().startswith(comment_style):
                    if logger:
                        logger.info(f"Skipped: Comment already exists after marker in {relative_path}")
                    return  # Comment already exists after marker, skip processing
                else:
                    content.insert(i + 1, relative_path_comment + "\n")
                    break
    else:
        # Insert the comment at the beginning of the file
        content.insert(0, relative_path_comment + "\n")

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(content)
    if logger:
        logger.info(f"Added comment for {relative_path}")

def get_log_file_path(log_directory, config_file):
    base_name = os.path.splitext(config_file)[0]
    log_file_name = f"{base_name}.log"
    log_file_path = os.path.join(log_directory, log_file_name)
    
    if os.path.exists(log_file_path):
        counter = 1
        while os.path.exists(f"{log_file_path}.{counter}"):
            counter += 1
        log_file_path = f"{log_file_path}.{counter}"
    
    return log_file_path

def process_directory(directory, file_types, project_root, exclude_folders, logger):
    """
    Processes each file within the given directory, applying comments based on file type,
    excluding specified folders. This function modifies files to include comments.

    :param directory: The directory to start processing from.
    :param file_types: Dictionary mapping file extensions to their comment styles.
    :param project_root: The root directory for calculating relative paths.
    :param exclude_folders: Folders to exclude from processing.
    :param logger: Logger object for logging actions.
    """
    exclude_paths = [os.path.normpath(os.path.join(project_root, folder)) for folder in exclude_folders]

    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in exclude_paths]
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_root)
            _, extension = os.path.splitext(file)
            extension_found = False

            for ext in sorted(file_types.keys(), key=len, reverse=True):
                if file.endswith(ext):
                    extension_found = True
                    comment_style = file_types[ext]['comment_style']
                    comment_after = file_types[ext].get('comment_after')
                    comment_end = file_types[ext].get('comment_end')
                    break

            if not extension_found:
                logger.info(f"Skipped: {relative_path} (Unsupported file type)")
                continue

            logger.info(f"Processing file: {relative_path}")
            logger.info(f"Comment style: {comment_style}")
            if comment_after:
                logger.info(f"Comment after: {comment_after}")

            process_file(file_path, comment_style, project_root, comment_after, comment_end, logger)

def create_project_config(project_type, project_name, project_path):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    project_types = config['project_types']

    if project_type in project_types:
        project_config = {
            "project_directory": project_path,
            "exclude_folders": config.get("exclude_folders", [".git", "vendor", "node_modules"]),
            "file_types": project_types[project_type]
        }

        project_name = project_name.replace(" ", "_")
        config_file_name = f"{project_name}.json"
        config_file_path = os.path.join('projects', config_file_name)

        os.makedirs('projects', exist_ok=True)  # Create the projects directory if it doesn't exist
        with open(config_file_path, 'w') as config_file:
            json.dump(project_config, config_file, indent=2)

        print(f"Created project configuration file: {config_file_path}")
    else:
        print(f"Unknown project type: {project_type}")
        
def process_directory_dryrun(directory, file_types, project_root, exclude_folders, logger):
    """
    Performs a dry run of processing the directory, simulating adding comments
    to each file based on its type, while excluding specified folders. It logs
    the intended actions to provide insight into what the script would do during
    an actual run.

    :param directory: The directory to start processing from.
    :param file_types: Dictionary mapping file extensions to their comment styles.
    :param project_root: Root directory of the project for calculating relative paths.
    :param exclude_folders: Folders to exclude from processing.
    :param logger: Logger object for logging actions.
    """
    exclude_paths = [os.path.normpath(os.path.join(project_root, folder)) for folder in exclude_folders]

    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in exclude_paths]
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_root)
            _, extension = os.path.splitext(file)
            extension_found = False

            for ext, details in sorted(file_types.items(), key=lambda item: len(item[0]), reverse=True):
                if file.endswith(ext):
                    extension_found = True
                    comment_style = details['comment_style']
                    comment_after = details.get('comment_after')
                    comment_end = details.get('comment_end')
                    break

            if not extension_found:
                logger.info(f"Skipped: {relative_path} (Unsupported file type)")
                continue

            logger.info(f"File: {relative_path}")
            logger.info(f"Comment style: {comment_style}")
            if comment_after:
                logger.info(f"Comment after: {comment_after}")

            comment = f"{comment_style} {relative_path}"
            if comment_end:
                comment += f" {comment_end}"

            # Simulating checking for existing comments
            with open(file_path, 'r') as f:
                if any(comment in line for line in f):
                    logger.info("Comment already exists. Skipping.")
                else:
                    logger.info(f"Comment to be added: {comment}")

            logger.info("=" * 40)

def main():
    parser = argparse.ArgumentParser(description="Add relative path comments to files.")
    parser.add_argument("config_file", nargs="?", help="Name of the configuration file (without .json extension)")
    parser.add_argument("--add", nargs=3, metavar=("project_type", "project_name", "project_path"),
                        help="Create a new project configuration")
    parser.add_argument("--dryrun", action="store_true", help="Perform a dry run without modifying files")
    args = parser.parse_args()

    if args.add:
        project_type, project_name, project_path = args.add
        create_project_config(project_type, project_name, project_path)
    elif args.config_file:
        config_file_path = os.path.join("projects", f"{args.config_file}.json")
        
        if not os.path.exists(config_file_path):
            print(f"Configuration file not found: {config_file_path}")
            return
        
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)

        log_directory = "logs"
        os.makedirs(log_directory, exist_ok=True)
        log_file_path = get_log_file_path(log_directory, args.config_file)

        logging.basicConfig(filename=log_file_path, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger()

        exclude_folders = config.get("exclude_folders", [".git", "vendor", "node_modules"])

        if args.dryrun:
            process_directory_dryrun(config['project_directory'], config['file_types'], config['project_directory'], exclude_folders, logger)
            print(f"Dry run completed. Check the log file: {log_file_path}")
        else:
            process_directory(config['project_directory'], config['file_types'], config['project_directory'], exclude_folders, logger)
            print(f"Processing completed. Check the log file: {log_file_path}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()