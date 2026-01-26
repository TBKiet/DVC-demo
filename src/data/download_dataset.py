import os
from datasets import load_dataset
from tqdm import tqdm

def download_and_extract_trashnet():
    print("Downloading TrashNet from Hugging Face...")
    # Load dataset from Hugging Face using a working mirror
    dataset = load_dataset("Zeeshan4349/trashnet", split="train")

    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)

    print(f"Extracting {len(dataset)} images to {output_dir}...")

    # Get features to map label IDs to names
    labels = dataset.features['label'].names

    for i, example in tqdm(enumerate(dataset), total=len(dataset)):
        image = example['image']
        label_id = example['label']
        label_name = labels[label_id]

        # Create class directory
        class_dir = os.path.join(output_dir, label_name)
        os.makedirs(class_dir, exist_ok=True)

        # Save image
        image_path = os.path.join(class_dir, f"{i}.jpg")
        image.save(image_path)

    print("Download and extraction complete!")

if __name__ == "__main__":
    download_and_extract_trashnet()
