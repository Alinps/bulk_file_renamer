from pathlib import Path
from dataclasses import dataclass
import os

from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

file_extentions = []






@dataclass
class RenameConfig:
    """Store user configuration for bulk file renaming."""

    prefix: str
    start_number: int
    number_width: int
    extensions: set[str]
    naming_mode: str



def configure_logging() -> logging.Logger:
    """
    Configure application logging.

    Creates a rotating log file inside the logs directory.

    Returns:
        logging.Logger: Configured application logger.
    """

    log_directory = Path(__file__).resolve().parent / "logs"
    log_directory.mkdir(exist_ok=True)

    log_file = log_directory / "app.log"

    logger = logging.getLogger("bulk_renamer")
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers.
    if logger.handlers:
        return logger

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger



def get_valid_folder_path(logger: logging.Logger) -> Path:
    while True:
        folder_input = input("Enter the folder path: ").strip()

        if not folder_input:
            print("Error: Folder path cannot be empty.")
            logger.warning("User provided an empty folder path.")
            continue

        folder_path = Path(folder_input).expanduser()

        if not folder_path.exists():
            print("Error: The specified path does not exist.")
            logger.warning("Folder does not exist: %s", folder_path)
            continue

        if not folder_path.is_dir():
            print("Error: The specified path is not a directory.")
            logger.warning("Path is not a directory: %s", folder_path)
            continue

        logger.info("Valid folder selected: %s", folder_path)
        return folder_path


def scan_files(
    folder_path: Path,
    logger: logging.Logger
) -> list[Path]:

    logger.info("Scanning folder: %s", folder_path)

    files = []

    try:
        for item in folder_path.iterdir():
            if item.is_file():
                files.append(item)

    except OSError:
        logger.exception("Failed to scan folder: %s", folder_path)
        raise

    files = sorted(files)

    logger.info("File scanning completed. Found %d files.", len(files))

    return files


def get_prefix() -> str:
    """Get a valid filename prefix from the user."""

    while True:
        prefix = input("Enter filename prefix: ").strip()

        if not prefix:
            print("Error: Prefix cannot be empty.")
            continue

        if prefix in {".", ".."}:
            print("Error: Invalid filename prefix.")
            continue

        if any(char in prefix for char in '<>:"/\\|?*'):
            print("Error: Prefix contains invalid filename characters.")
            continue

        return prefix


def get_start_number() -> int:
    """Get a valid starting number."""

    while True:
        user_input = input("Enter starting number: ").strip()

        try:
            number = int(user_input)

            if number < 0:
                print("Error: Starting number cannot be negative.")
                continue

            return number

        except ValueError:
            print("Error: Please enter a valid integer.")




def get_number_width() -> int:
    """Get the number of digits for sequential numbering."""

    while True:
        user_input = input("Enter numbering width (e.g. 3): ").strip()

        try:
            width = int(user_input)

            if width < 1:
                print("Error: Width must be at least 1.")
                continue

            return width

        except ValueError:
            print("Error: Please enter a valid integer.")




def get_extensions() -> set[str]:
    """Get the file extensions selected by the user."""

    while True:
        user_input = input(
            "Enter extensions separated by commas (e.g. jpg, png): "
        ).strip()

        if not user_input:
            print("Error: Please select at least one extension.")
            continue

        extensions = set()

        for extension in user_input.split(","):
            extension = extension.strip().lower()

            if not extension:
                continue

            if not extension.startswith("."):
                extension = f".{extension}"

            extensions.add(extension)

        if not extensions:
            print("Error: No valid extensions provided.")
            continue

        if any(
            not extension[1:].replace("_", "").replace("-", "").isalnum()
            for extension in extensions
        ):
            print("Error: Invalid file extension.")
            continue

        return extensions







def get_rename_config() -> RenameConfig:
    """Collect all user configuration."""

    print("\n--- Rename Configuration ---")

    naming_mode = get_naming_mode()
    prefix = get_prefix()
    start_number = get_start_number()
    number_width = get_number_width()
    extensions = get_extensions()

    return RenameConfig(
        prefix=prefix,
        start_number=start_number,
        number_width=number_width,
        extensions=extensions,
        naming_mode=naming_mode
    )





def generate_rename_plan(
    files: list[Path],
    config: RenameConfig,
    logger: logging.Logger
) -> list[tuple[Path, Path]]:
    """
    Generate old and new filename pairs.

    Args:
        files: Files discovered in the directory.
        config: User-provided renaming configuration.

    Returns:
        list[tuple[Path, Path]]: Pairs of original and proposed paths.
    """

    rename_plan = []

    counter = config.start_number
    excluded_counter = 0

    for file in files:

        extension = file.suffix.lower()
        

        if extension not in config.extensions:
            excluded_counter  +=1
            continue

        formatted_number = (
            f"{counter:0{config.number_width}d}"
        )

        new_filename = (
            f"{config.prefix}_{formatted_number}{file.suffix}"
        )

        new_path = file.parent / new_filename

        rename_plan.append((file, new_path))

        counter += 1

        logger.info(
            "Sequential rename plan generated. Total files: %d",
            len(rename_plan)
        )

    return rename_plan




def confirm_rename() -> bool:
    """
    Ask the user whether to proceed with renaming.

    Returns:
        bool: True if the user confirms, otherwise False.
    """

    while True:
        choice = input(
            "\nDo you want to proceed with renaming? (y/n): "
        ).strip().lower()

        if choice == "y":
            return True

        if choice == "n":
            return False

        print("Invalid choice. Please enter 'y' or 'n'.")






def file_summary(files: List[Path]) -> dict[str, int]:

    summary = {
        category:0
        for category in file_extentions
    }

    for item in files:
        summary[item.suffix.lower()] +=1

    return summary








def display_rename_preview(
    rename_plan: list[tuple[Path, Path]]
) -> None:
    """
    Display the proposed filename changes.

    Args:
        rename_plan: Original and proposed file path pairs.
    """

    if not rename_plan:
        print("\nNo files found matching the selected extensions.")
        return

    print("\n" + "=" * 75)
    print("                    RENAME PREVIEW")
    print("=" * 75)

    print(f"\n{'ORIGINAL NAME':<35} {'NEW NAME':<35}")
    print("-" * 75)

    for old_path, new_path in rename_plan:
        print(f"{old_path.name:<35} -> {new_path.name}")

    print("-" * 75)

    print(f"Total files to rename: {len(rename_plan)}")
    print("=" * 75)


    

    for old_path, new_path in rename_plan:
        print(f"{old_path.name}  ->  {new_path.name}")

    print(f"\nTotal files selected: {len(rename_plan)}")





def find_collisions(
    rename_plan: list[tuple[Path, Path]]
) -> list[Path]:
    """
    Find destination paths that already exist.

    Args:
        rename_plan: Original and proposed path pairs.

    Returns:
        list[Path]: Destination paths that already exist.
    """

    collisions = []

    for old_path, new_path in rename_plan:

        if old_path == new_path:
            continue

        if new_path.exists():
            collisions.append(new_path)

    return collisions




def display_collisions(collisions: list[Path]) -> None:
    """
    Display destination filename conflicts.

    Args:
        collisions: List of existing destination paths.
    """

    if not collisions:
        print("\nNo filename collisions detected.")
        return

    print("\nWARNING: Filename collisions detected!")

    for path in collisions:
        print(f"Destination already exists: {path.name}")

    print("\nPlease change the prefix or starting number.")




def execute_rename(
    rename_plan: list[tuple[Path, Path]],
    logger: logging.Logger
) -> tuple[int, list[str]]:
    """
    Execute the rename plan without overwriting existing files.

    Args:
        rename_plan: Original and proposed path pairs.

    Returns:
        tuple[int, list[str]]:
            Number of successfully renamed files and error messages.
    """

    success_count = 0
    errors = []

    for old_path, new_path in rename_plan:

        if old_path == new_path:
            continue

        try:
            # Create the destination without replacing an existing file.
            os.link(old_path, new_path)

            try:
                # Remove the original filename.
                old_path.unlink()
                logger.info(
                        "File renamed successfully: %s -> %s",
                        old_path.name,
                        new_path.name
                    )

            except OSError:
                # Attempt to remove the newly created link if cleanup fails.
                new_path.unlink(missing_ok=True)
                raise

            success_count += 1

        except OSError as error:
            logger.exception(
                "Failed to rename file: %s -> %s",
                old_path,
                new_path
            )

            errors.append(error_message)

    return success_count, errors



def get_naming_mode() -> str:
    """Ask the user to select a naming mode."""

    while True:
        print("\nSelect naming mode:")
        print("1. Sequential naming")
        print("2. Date-based naming")

        choice = input("Enter your choice (1/2): ").strip()

        if choice == "1":
            return "sequential"

        if choice == "2":
            return "date"

        print("Invalid choice. Please select 1 or 2.")






def get_modification_date(
    file_path: Path,
    logger: logging.Logger
) -> str:

    try:
        timestamp = file_path.stat().st_mtime
        modification_date = datetime.fromtimestamp(timestamp)

        return modification_date.strftime("%Y-%m-%d")

    except OSError:
        logger.exception(
            "Unable to retrieve modification date: %s",
            file_path
        )
        raise



def generate_date_based_plan(
    files: list[Path],
    config: RenameConfig,
    logger: logging.Logger
) -> list[tuple[Path, Path]]:
    """
    Generate a rename plan using file modification dates.

    Numbering restarts for each modification date.

    Args:
        files: Files discovered in the directory.
        config: User-provided rename configuration.

    Returns:
        list[tuple[Path, Path]]: Original and proposed path pairs.
    """

    files_by_date = {}

    # Group selected files by modification date.
    for file in files:

        extension = file.suffix.lower()

        if extension not in config.extensions:
            continue

        modification_date = get_modification_date(file)

        files_by_date.setdefault(
            modification_date, []
        ).append(file)

    rename_plan = []

    # Generate filenames for each date.
    for date, date_files in sorted(files_by_date.items()):

        counter = config.start_number

        for file in date_files:

            formatted_number = (
                f"{counter:0{config.number_width}d}"
            )

            new_filename = (
                f"{date}_{config.prefix}_"
                f"{formatted_number}{file.suffix}"
            )

            new_path = file.parent / new_filename

            rename_plan.append((file, new_path))

            counter += 1

            logger.info(
            "Date-based rename plan generated. Total files: %d",
            len(rename_plan)
        )

    return rename_plan








def main() -> None:
    """Application entry point."""


    logger = configure_logging()

    logger.info("Application started.")

    try:

        print("Bulk File Renaming Tool")

        folder_path = get_valid_folder_path(logger)
        print(f"\nSelected folder: {folder_path}")

        files = scan_files(folder_path, logger)
        print(f"\nTotal files found: {len(files)}")

    

        config = get_rename_config()

        if config.naming_mode == "sequential":
            rename_plan = generate_rename_plan(files, config, logger)

        else:
            rename_plan = generate_date_based_plan(files, config, logger)

        display_rename_preview(rename_plan)

        if not rename_plan:
            return

        # Check for existing destination files.
        collisions = find_collisions(rename_plan)

        if collisions:
            display_collisions(collisions)
            print("\nRenaming aborted to protect existing files.")
            return

        # Ask for user confirmation.
        if not confirm_rename():
            print("\nRenaming operation cancelled.")
            return

        # Execute the renaming operation.
        success_count, errors = execute_rename(rename_plan, logger)

        print("\n--- Rename Summary ---")
        print(f"Successfully renamed: {success_count}")

        if errors:
            print(f"Failed operations: {len(errors)}")

            for error in errors:
                print(error)

        else:
            print("All files were renamed successfully.")

        logger.info("Application completed successfully.")


    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        logger.warning("Application interrupted by user.")

    except Exception:
        print("An unexpected error occurred. Check logs/app.log for details.")
        logger.exception("Unexpected application error.")

    finally:
        logger.info("Application terminated.")



if __name__ == "__main__":
    main()








