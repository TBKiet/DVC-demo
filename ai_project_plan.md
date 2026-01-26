# AI Engineering Project Blueprint: "EcoVision" - Waste Classification System

This project is designed to give you hands-on experience with the modern MLOps stack. You will build a computer vision application that creates value by helping sort recyclable waste.

## 🛠 Tech Stack & Why

- **Data Version Control (DVC)**: To treat data like code. Reproducibility starts with data versioning.
- **PyTorch**: The industry-standard research-to-production deep learning framework.
- **Weights & Biases (W&B)**: To track experiments, visualize loss curves, and manage model artifacts.
- **Streamlit**: For rapid prototyping of the ML application frontend.
- **Docker**: To ensure the application runs consistently on any machine (setup once, run anywhere).

---

## 📅 Phase 1: Project Setup & Data Engineering

**Goal**: Initialize the environment and version control the data.

1.  **Project Structure Setup**
    - Create a clean folder structure (`src`, `data`, `notebooks`, `models`).
    - Initialize Git (`git init`).
2.  **Virtual Environment**
    - Manage dependencies with `conda` or `venv`.
    - Create `requirements.txt`.
3.  **Data Versioning with DVC**
    - Initialize DVC (`dvc init`).
    - Download the **TrashNet** dataset (approx 2.5k images of Glass, Paper, Cardboard, Plastic, Metal, Trash).
    - Track data: `dvc add data/raw`.
    - Commit the `.dvc` file to Git (Data is not in Git, only the _pointer_ is).

## 🧪 Phase 2: Model Training & Tracking

**Goal**: Train a robust classifier and track experiments.

1.  **Data Pipeline**
    - Write a PyTorch `Dataset` class to load images.
    - Implement data augmentation (Flip, Rotation, Normalization) to improve generalization.
    - Split data into Train/Val/Test (e.g., 80/10/10).
2.  **Model Architecture**
    - Use **Transfer Learning**: Download a pre-trained **ResNet18** (or EfficientNet).
    - Replace the final fully connected layer to match our 6 classes.
3.  **Experiment Tracking with W&B**
    - Set up a Free W&B account.
    - In your training loop:
      ```python
      wandb.init(project="ecovision")
      wandb.log({"loss": loss, "accuracy": acc})
      ```
    - Compare runs with different learning rates or augmentations.

## 📦 Phase 3: Application & Deployment

**Goal**: Serve the model to users.

1.  **Inference Engine**
    - Write a script to load the best model (setup `torch.load`).
    - Preprocess input images exactly as done during training.
2.  **Streamlit Visualization**
    - Create `app.py`.
    - Allow users to upload an image.
    - Display prediction and confidence bars.
3.  **Docker Containerization**
    - Draft a `Dockerfile`.
    - Base image: `python:3.9-slim`.
    - Copy code and `requirements.txt`.
    - Run command: `streamlit run app.py`.
4.  **Run & Verify**
    - Build: `docker build -t ecovision .`
    - Run: `docker run -p 8501:8501 ecovision`

---

## 🚀 Recommended Next Steps

1.  **Create the directory**: `mkdir -p ecovision/data ecovision/src`
2.  **Install tools**: `pip install dvc wandb torch torchvision streamlit`
3.  **Get Data**: Download the dataset and start with Phase 1.
