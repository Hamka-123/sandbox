from pathlib import Path
from file_utils import create_project_directories


def main():
    # Determine the project directory
    project_dir = Path(__file__).resolve().parent

    # Display the project directory
    print(f"Project directory: {project_dir}")

    # Create data and output directories
    create_project_directories(project_dir)


if __name__ == "__main__":
    main()
