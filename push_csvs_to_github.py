from pathlib import Path
import shutil
import subprocess
from datetime import datetime

# Folder where the daily CSV files are created
SOURCE_FOLDER = Path(r"C:\Users\aronc\Documents\solar_test_files")

# Your local GitHub repo folder
REPO_FOLDER = Path(r"C:\Users\aronc\Documents\GitHub\solar_live_data")

# Folder inside the repo where CSVs will be stored
DEST_FOLDER = REPO_FOLDER / "data"

CSV_PATTERN = "gpg_*.csv"

DEST_FOLDER.mkdir(parents=True, exist_ok=True)

# Copy CSV files into repo/data
for csv_file in SOURCE_FOLDER.glob(CSV_PATTERN):
    dest_file = DEST_FOLDER / csv_file.name
    shutil.copy2(csv_file, dest_file)
    print(f"Copied {csv_file.name}")

# Git add, commit, push
subprocess.run(["git", "add", "data"], cwd=REPO_FOLDER, check=True)

commit_message = f"Update solar CSV data {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# Commit may fail if nothing changed, so handle it
commit = subprocess.run(
    ["git", "commit", "-m", commit_message],
    cwd=REPO_FOLDER,
    text=True,
    capture_output=True
)

if commit.returncode != 0:
    print("No new changes to commit.")
else:
    print(commit.stdout)
    subprocess.run(["git", "push"], cwd=REPO_FOLDER, check=True)
    print("SUCCESS: CSV files pushed to GitHub.")