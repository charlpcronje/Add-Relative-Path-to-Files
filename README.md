# Add Relative Path to Files

This Python script scans through a project directory and adds comments with the relative file path to the first line of each file matching the specified file types in the configuration file. It supports a wide array of programming languages and file types, offering a versatile tool for code documentation and reference.

## Features

- **Dynamic Commenting Based on File Type**: Adds comments to files according to their type, with customizable comment styles and placements.
- **Support for Multiple Programming Languages**: Handles various languages and frameworks by reading their file types and comment styles from a configuration file.
- **Custom Comment Placement**: Supports specifying a marker string (`comment_after`) to determine where within the file the comment should be added, accommodating language-specific conventions like PHP's `<?php`.
- **Block Comment Handling**: Manages block comments with start (`comment_style`) and end (`comment_end`) tags, suitable for languages that use block comments (e.g., CSS, HTML).
- **Prevention of Duplicate Comments**: Checks for existing comments to avoid duplicating the relative path comment in files.
- **Configurable Project Types**: Allows defining different project types with their associated file extensions and comment styles in a `config.json` file.
- **Directory Exclusion**: Excludes specified directories (e.g., `.git`, `vendor`, `node_modules`) from being processed to prevent altering third-party or non-source code files.
- **Flexible Configuration**: Enables specifying different project configurations through JSON files, supporting various project setups.
- **Logging**: Logs actions taken (or to be taken in dry run mode) for each file, providing insights into the script's operations.
- **Command-Line Interface (CLI)**: Offers a CLI for easy execution, configuration selection, and operation mode toggling (actual run vs. dry run).
- 
## Supported Project and File Types

The script can process a wide variety of project types, each associated with specific file types. Below is a comprehensive list of supported project types and a selection of file types they include, as defined in the `config.json`:

(Note: Only a selection is shown here due to space constraints. The script supports many more as defined in the provided `config.json`.)

- **Node**: `.js`
- **React**: `.jsx`, `.css`, `.js`, `.ts`, `.html`
- **Vue/Nuxt**: `.vue`, `.js`, `.ts`, `.css`, `.html`
- **Laravel**: `.php` (with special handling for `<?php`), `.blade.php`
- **Python/Flask**: `.py`
- **Web (Generic)**: `.html`, `.js`, `.css`
- **Angular**: `.ts`, `.html`, `.css`, `.scss`, `.less`
- **Svelte**: `.svelte`, `.js`, `.ts`, `.css`, `.scss`, `.less`
- **...and many more**: Including `ember`, `ruby-on-rails`, `aspnet-razor`, `java-jsp`, `go`, `rust`, `c++`, `c#`, `swift`, `kotlin`, `dart`, `elixir`, `scala`, `clojure`, `haskell`, `elm`, `julia`, `lua`, `perl`, `r`, `groovy`, `markdown`, `restructuredtext`, `asciidoc`, `latex`.

## Command-Line Arguments

- `config_file`: Specifies the name of the project configuration file (without the `.json` extension) to use for processing files in a project.
- `--add [project_type] [project_name] [project_path]`: Creates a new project configuration file based on the specified type, name, and path. This configuration file is saved in the `projects` directory and includes default directory exclusions.
- `--dryrun`: Executes the script in dry run mode, logging the actions that would be taken without actually modifying any files. Useful for verifying the expected changes before committing them.

## In the case of `.blade.php` and `.php` where all `.blade.php` are `.php` files too

Regarding the case where both `.php` and `.blade.php` file types are specified in the same configuration file:

- In the `config.json` file, the `.blade.php` file type is specified with a different commenting style (`{{--` and `--}}`) compared to the regular `.php` file type (`//`). This is because Blade templates in Laravel use a different syntax for comments.
- When the script processes the files, it will first check if the file extension matches `.blade.php`. If it does, it will use the commenting style specified for `.blade.php` (`{{--` and `--}}`). If the file extension matches `.php` but not `.blade.php`, it will use the commenting style specified for `.php` (`//`).
- This means that if both `.php` and `.blade.php` are specified in the configuration file, the script will prioritize the `.blade.php` file type for Blade template files and use the appropriate commenting style. For regular PHP files, it will use the commenting style specified for `.php`.
- By having separate entries for `.php` and `.blade.php` in the configuration file, the script ensures that the correct commenting style is applied based on the specific file type, preventing any potential issues with breaking the file syntax.
- It's important to note that `.blade.php` files are indeed PHP files, but they are used specifically for Blade templates in Laravel and have a different commenting syntax. The script takes this into account and handles the commenting accordingly based on the file extension.
- I hope this clarifies how the script handles the case where both `.php` and `.blade.php` are specified in the configuration file. Let me know if you have any further questions!

## Folder Structure

The script expects the following folder structure:

```sh
.
├── app.py
├── config.json
├── README.md
└── projects
  ├── project_one.json
  └── project_two.json
```

- `app.py`: The main Python script.
- `config.json`: The configuration file containing the project types and their corresponding file types and commenting styles.
- `README.md`: The readme file with instructions and information about the script.
- `projects`: A directory containing the individual project configuration files.
  - `project_one.json`, `project_two.json`, etc.: Configuration files for each project, specifying the project directory and file types.



## Usage

### Creating a Project Configuration

To create a new project configuration using the `--add` flag:

```sh
python app.py --add react my_react_project /path/to/my/react/project
```

This command will create a new configuration file in the `projects` directory for a React project located at the specified path. The configuration file will include the default file types and comment styles for React projects, as well as default directory exclusions.

### Running the Script

To add comments to your project files:

```sh
python app.py my_react_project
```

Replace `my_react_project` with the name of your project configuration file (without the `.json` extension). The script will process the files according to the configuration, adding comments with relative paths.

### Dry

 Run

To perform a dry run and see what changes would be made without actually modifying any files:

```sh
python app.py my_react_project --dryrun
```

Check the generated log file in the `logs` directory to review the actions that would be taken.
```


# Add Relative Path to Files

This Python script scans through a project directory and adds comments with the relative file path to the first line of each file matching the specified file types in the configuration file.

## Features




## Usage

1. Clone the repository:

```sh
git clone https://github.com/charlpcronje/Add-Relative-Path-to-Files.git
```

2. Navigate to the project directory:

```sh
cd Add-Relative-Path-to-Files
```

3. Create a project configuration file in the `projects` directory:
- Create a new JSON file with a name representing your project (e.g., `project_one.json`).
- Inside the JSON file, specify the project directory and file types using the following format:
  ```json
  {
    "project_directory": "/path/to/your/project",
    "file_types": {
      ".ext1": {
        "comment_style": "comment_style1"
      },
      ".ext2": {
        "comment_style": "comment_style2",
        "comment_after": "string_to_look_for"
      }
    }
  }
  ```
  Replace `/path/to/your/project` with the actual path to your project directory, and customize the file types and commenting styles according to your project's requirements.

  Or use the config creator option by running the following command:
  
  ```sh
  python app.py --add {project_type} {project_name} {/path/to/project}

  ```
  Replace `{project_type}` with the desired project type (e.g., `react`), `{project_name}` with the name of your project, and `{/path/to/project}` with the path to your project directory.

4. Run the script with the configuration file:

```sh
python app.py project_one
```

Replace `project_one` with the name of your project configuration file (without the `.json` extension).

5. The script will scan through your project directory and add comments with the relative file path to the first line or after the specified `comment_after` string of each matching file.

## Contact

For any queries or assistance, please reach out to:

- **Name**: Charl Cronje
- **Email**: [charl@cronje.me](mailto:charl@cronje.me)
- **LinkedIn**: [https://www.linkedin.com/in/charlpcronje](https://www.linkedin.com/in/charlpcronje)