# Add Relative Path to Files

This Python script scans through a project directory and adds comments with the relative file path to the first line of each file matching the specified file types in the configuration file.

## Features

- Reads file types and commenting styles from a JSON configuration file
- Supports specifying a string to look for and add the comment on the next line (useful for files like ".php" where the comment must be added below the `<?php` opening tag)
- Handles file types that require a closing comment tag, such as `.blade.php` and `.html`
- Avoids adding duplicate comments if the comment already exists in the file
- Allows specifying the configuration file as a command-line argument

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