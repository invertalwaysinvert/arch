#!/bin/python
import os
import shutil
import subprocess

subprocess.run(
    "git clone --depth 1 https://github.com/AstroNvim/AstroNvim /home/arch/.config/nvim",
    shell=True,
    check=True,
    capture_output=True,
    text=True,
)
subprocess.run(
    "git clone https://github.com/invertalwaysinvert/arch",
    shell=True,
    check=True,
    capture_output=True,
    text=True,
)


def overwrite_files(source_folder, target_folder):
    # Iterate over all files in the source folder
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, source_folder)
            target_path = os.path.join(target_folder, relative_path)

            # Create the target directory if it doesn't exist
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            # Overwrite the file in the target folder
            shutil.copy2(source_path, target_path)
            print(f"Overwritten: {target_path}")


# Usage example
source_folder = "arch/airootfs/home/arch/.config/nvim"
target_folder = ".config/nvim"

overwrite_files(source_folder, target_folder)
shutil.rmtree("arch")
shutil.rmtree("nvim.py")
