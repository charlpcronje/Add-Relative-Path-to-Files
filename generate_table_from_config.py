import json

def generate_markdown_table(config_path, output_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    markdown_table = "Project Type | File Extensions\n"
    markdown_table += "--- | ---\n"

    for project_type, file_types in config["project_types"].items():
        extensions = ", ".join(file_types.keys())
        markdown_table += f"{project_type} | {extensions}\n"

    with open(output_path, "w") as md_file:
        md_file.write(markdown_table)

if __name__ == "__main__":
    config_path = 'config.json'  # Path to your config.json
    output_path = 'types.md'     # Desired output markdown file
    generate_markdown_table(config_path, output_path)
    print(f"Markdown table has been generated in {output_path}")
