import os
import subprocess
import sys
from pathlib import Path


def create_venv(venv_dir=".venv"):
    venv_dir = Path(venv_dir)
    # Create the virtual environment
    if not os.path.exists(venv_dir):
        subprocess.run([sys.executable, "-m", "venv", venv_dir.name], check=True)
        print(f"Virtual environment created at {venv_dir}")
    else:
        print(f"Virtual environment already exists at {venv_dir}")

    if venv_dir.joinpath("Scripts").exists():
        subprocess.run([f"{venv_dir.name}/Scripts/activate"], check=True)
    else:
        subprocess.run([f"source {venv_dir.name}/bin/activate"], check=True)


def install_requirements(venv_dir="venv", requirements_file="requirements.txt"):
    # Path to pip in the virtual environment
    pip_executable = (
        os.path.join(venv_dir, "Scripts", "pip") if os.name == "nt" else os.path.join(venv_dir, "bin", "pip")
    )

    if os.path.exists(requirements_file):
        subprocess.run([pip_executable, "install", "-r", requirements_file], check=True)
        print(f"Installed requirements from {requirements_file}")
    else:
        print(f"Requirements file {requirements_file} not found.")


if __name__ == "__main__":
    venv_directory = ".venv"  # Change as needed
    req_file = "requirements.txt"  # Change as needed

    create_venv(venv_directory)
    install_requirements(venv_directory, req_file)
