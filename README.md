
# Bulk File Renaming Tool

A Python-based command-line application that simplifies renaming multiple files in a directory using configurable naming patterns.

The application supports sequential numbering and modification-date-based naming, with a preview and confirmation process before applying changes.

## Features

- **Folder Validation:** Validates the directory path provided by the user.
- **File Scanning:** Scans files in the selected directory.
- **Custom Prefix:** Allows users to specify a filename prefix.
- **Sequential Naming:** Renames files using sequential numbering.
- **Custom Starting Number:** Allows users to choose the starting number.
- **Custom Number Width:** Supports zero-padded numbering.
- **File Type Filtering:** Allows users to select specific file extensions.
- **Date-Based Naming:** Generates filenames using file modification dates.
- **Preview:** Displays proposed filename changes before execution.
- **Collision Prevention:** Checks whether destination filenames already exist.
- **Safe Renaming:** Prevents accidental overwriting during file operations.
- **Logging:** Records application events and errors.
- **Log Rotation:** Automatically rotates log files to control their size.
- **Exception Handling:** Handles file operation errors and unexpected application failures.

## Technologies Used

- Python
- pathlib
- os
- logging
- RotatingFileHandler
- datetime

## Project Structure

The following is a suggested structure for the project. Adapt filenames to match your actual implementation.

```text
bulk-file-renaming-tool/
│
├── main.py
│
├── logs/
│   └── app.log
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.10 or higher
- No external dependencies are required for the core application.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Navigate to the project directory

```bash
cd bulk-file-renaming-tool
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

If your project uses only Python standard-library modules, no installation is necessary.

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

The application guides the user through the renaming process interactively.

### 1. Select a folder

Enter the directory containing the files you want to rename.

```text
Enter the folder path: /home/user/photos
```

### 2. Configure the naming options

Provide the required configuration:

- Filename prefix
- Starting number
- Number width
- File extensions
- Naming mode

### 3. Preview the changes

The application displays the original and proposed filenames.

Example:

```text
Original Filename       New Filename
------------------------------------------------
IMG_001.jpg             photo_001.jpg
IMG_002.jpg             photo_002.jpg
IMG_003.jpg             photo_003.jpg
```

### 4. Confirm the operation

The application asks for confirmation before renaming files.

No changes are made during the preview stage.

### 5. View the execution summary

After execution, the application displays the number of successfully renamed files and any failures.

## Naming Modes

### Sequential Naming

Generates filenames using a common prefix and sequential numbering.

Example:

```text
Original Filename       New Filename
------------------------------------------------
IMG_001.jpg             photo_001.jpg
IMG_002.jpg             photo_002.jpg
IMG_003.jpg             photo_003.jpg
```

### Date-Based Naming

Generates filenames using the file modification date.

Example:

```text
Original Filename       New Filename
------------------------------------------------
IMG_001.jpg             2026-11-21_photo_001.jpg
IMG_002.jpg             2026-11-21_photo_002.jpg
IMG_003.jpg             2026-11-22_photo_001.jpg
```

Numbering restarts for each date.

**Note:** The application uses the file's modification date, not necessarily the original photo capture date stored in image metadata.

## Logging

The application uses Python's built-in logging module to record important events.

Log files are stored in:

```text
logs/app.log
```

The logging system records:

- Application startup and termination
- Folder selection
- File scanning results
- Rename plan generation
- Successful rename operations
- Failed file operations
- Unexpected application errors

### Log Rotation

The application uses `RotatingFileHandler`.

Current configuration:

```python
maxBytes=1_000_000
backupCount=3
```

This limits the active log file to approximately 1 MB and retains up to three backup log files.

## Exception Handling

The application handles errors such as:

- Invalid folder paths
- Missing directories
- Permission errors
- File operation failures
- Modification-date retrieval failures
- User interruptions using Ctrl+C
- Unexpected application exceptions

Errors are recorded in the log file to support troubleshooting.

## Safety Considerations

- The application previews changes before execution.
- Existing destination files are checked to prevent overwriting.
- Individual file operation failures are recorded.
- Failed operations are reported in the execution summary.

**Important:** A batch rename operation is not transactional. If some files are renamed successfully and a later operation fails, earlier changes are not automatically rolled back.

## Testing

Automated unit testing with `pytest` is planned for Phase 9.

The intended test coverage includes:

- Folder validation
- File discovery
- Configuration validation
- Sequential filename generation
- Date-based filename generation
- Preview generation
- Destination collision detection
- Rename execution
- Error handling

## Future Improvements

Potential enhancements include:

- Automated unit testing with pytest
- Improved modular architecture
- Recursive directory scanning
- Undo and rollback support
- EXIF-based photo capture date extraction
- Graphical user interface using PySide6

## Learning Outcomes

This project demonstrates practical Python development concepts:

- Object-oriented and modular programming
- Functions and reusable components
- pathlib and filesystem operations
- Dataclasses and configuration management
- String formatting
- Exception handling
- Logging and log rotation
- Safe file operations
- Command-line application development

## License

This project is available for educational and personal use.


