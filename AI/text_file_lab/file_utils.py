from pathlib import Path


def create_project_directories(project_dir):
    """
    Create directories required by the project.
    """
    # Ensure project_dir is a Path object
    project_path = Path(project_dir)

    # Define paths for data and output directories
    data_dir = project_path / "data"
    output_dir = project_path / "output"

    # Create the directories if they do not already exist
    data_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Display a success message
    print("Project directories created successfully.")
