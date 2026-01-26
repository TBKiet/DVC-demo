# EcoVision ♻️

**Modern Waste Classification System**

This project demonstrates a complete MLOps workflow for a computer vision application, including Data Version Control (DVC), PyTorch training, Experiment Tracking (W&B), and Dockerized Deployment.

## 📂 Project Structure

- `data/`: Contains dataset (managed by DVC).
- `models/`: Stores trained model weights.
- `src/`: Source code for training and inference.
  - `train.py`: PyTorch training script with W&B logging.
  - `app.py`: Streamlit web application.
- `Dockerfile`: Configuration for containerizing the app.

## 🚀 Getting Started

### 1. Environment Setup

Dependencies have been installed. If you need to reinstall:

```bash
pip install -r requirements.txt
```

### 2. Data Version Control (DVC)

The TrashNet dataset is already downloaded in `data/raw` and tracked by DVC.
To see the DVC status:

```bash
dvc status
```

### 3. Train the Model 🧠

Before training, log in to Weights & Biases:

```bash
wandb login
```

Run the training script (Mac users: script is optimized for MPS/Metal acceleration):

```bash
python src/train.py
```

This will:

- Train a ResNet18 model on the TrashNet dataset.
- Log metrics (Loss, Accuracy) to W&B.
- Save the best model to `models/ecovision_resnet18.pth`.

### 4. Run the App 🌐

Start the Streamlit interface:

```bash
streamlit run src/app.py
```

Upload an image to test the classification!

### 5. Docker Deployment 🐳

Build and run the container:

```bash
docker build -t ecovision .
docker run -p 8501:8501 ecovision
```

Access at `http://localhost:8501`.

## 🛠 Tech Stack

- **Data**: [DVC](https://dvc.org/)
- **Model**: [PyTorch](https://pytorch.org/) (ResNet18 Transfer Learning)
- **Tracking**: [Weights & Biases](https://wandb.ai/)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Container**: [Docker](https://www.docker.com/)
