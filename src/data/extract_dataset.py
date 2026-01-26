import zipfile
import os
from pathlib import Path

def extract_data():
    zip_path = Path("data/raw/dataset-original.zip")
    extract_to = Path("data/raw")

    if not zip_path.exists():
        print(f"File {zip_path} not found!")
        return

    print("Extracting dataset...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    print("Extraction complete.")

    # Check structure
    dataset_dir = extract_to / "dataset-original"
    if dataset_dir.exists():
        print(f"Moving files from {dataset_dir} to {extract_to}...")
        for item in dataset_dir.iterdir():
            if item.is_dir():
                target = extract_to / item.name
                if target.exists():
                    # Merge or skip
                    pass
                else:
                    item.rename(target)
        # Cleanup
        dataset_dir.rmdir()

    # Remove zip file
    # zip_path.unlink() # Keep it or remove? DVC usually tracks the data directory, we can remove zip.
    print("Cleaned up.")

if __name__ == "__main__":
    extract_data()
