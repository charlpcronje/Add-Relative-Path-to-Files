import os
import json
import argparse

def process_file(file_path, comment_style, comment_after=None, comment_end=None):
    with open(file_path, 'r') as file:
        content = file.readlines()

    if comment_after:
        comment_exists = False
        for i, line in enumerate(content):
            if comment_after in line:
                if i + 1 < len(content) and content[i + 1].strip().startswith(comment_style):
                    comment_exists = True
                    break
                else:
                    comment = f"{comment_style} {os.path.relpath(file_path)}"
                    if comment_end:
                        comment += f" {comment_end}"
                    content.insert(i + 1, comment + "\n")
                    break
        if comment_exists:
            return  # Comment already exists, skip processing
    else:
        if content and content[0].strip().startswith(comment_style):
            return  # Comment already exists, skip processing
        comment = f"{comment_style} {os.path.relpath(file_path)}"
        if comment_end:
            comment += f" {comment_end}"
        content.insert(0, comment + "\n")

    with open(file_path, 'w') as file:
        file.writelines(content)

def process_directory(directory, file_types):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            _, extension = os.path.splitext(file)

            if extension in file_types:
                comment_style = file_types[extension]['comment_style']
                comment_after = file_types[extension].get('comment_after')
                comment_end = file_types[extension].get('comment_end')
                process_file(file_path, comment_style, comment_after, comment_end)

def create_project_config(project_type, project_name, project_path):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    project_types = config['project_types']

    if project_type in project_types:
        project_config = {
            "project_directory": project_path,
            "file_types": project_types[project_type]
        }

        project_name = project_name.replace(" ", "_")
        config_file_name = f"{project_name}.json"

        with open(config_file_name, 'w') as config_file:
            json.dump(project_config, config_file, indent=2)

        print(f"Created project configuration file: {config_file_name}")
    else:
        print(f"Unknown project type: {project_type}")
        
def main():
    parser = argparse.ArgumentParser(description='Add relative path comments to files.')
    parser.add_argument('config_file', help='Name of the configuration file (without .json extension)')
    args = parser.parse_args()

    config_file_path = os.path.join('projects', f'{args.config_file}.json')

    if not os.path.exists(config_file_path):
        print(f"Configuration file not found: {config_file_path}")
        return

    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)

    project_directory = config['project_directory']
    file_types = config['file_types']

    process_directory(project_directory, file_types)

if __name__ == '__main__':
    main()