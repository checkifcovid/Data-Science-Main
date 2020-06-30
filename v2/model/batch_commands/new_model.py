import os
import sys
import subprocess
from pathlib import Path
sys.path.append("././") # go up 2 levels

def train_new_model():
    """
    Trains and saves a new model.
    """
    # 1. Get the newest data & Create a new model
    file_path = Path("model/create.py")
    command = f"python3 {file_path}"
    subprocess.call(command, shell=True)


    # 2. Download that model
    file_path = Path("model/get_most_recent_model.py")
    command = f"python3 {file_path}"
    subprocess.call(command, shell=True)

    # The method below didn't work neatly...
    # with open(file_path, "r") as fh:
    #         exec(fh.read())

if __name__ == "__main__":
    train_new_model()
