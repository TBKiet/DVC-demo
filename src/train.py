import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
import wandb
import os

def train():
    # Hyperparameters
    BATCH_SIZE = 32
    LR = 0.001
    EPOCHS = 5

    # Initialize W&B
    wandb.init(project="ecovision", config={
        "learning_rate": LR,
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "architecture": "resnet18"
    })

    # Data Augmentation & Loading
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    data_dir = 'data/raw' # Or split into train/val

    # Note: You might need to manually split data or use SubsetRandomSampler
    # For simplicity, assuming data/raw has class folders

    full_dataset = datasets.ImageFolder(data_dir, data_transforms['train'])

    # Simple split
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])

    dataloaders = {
        'train': torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True),
        'val': torch.utils.data.DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    }

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Model Setup
    model = models.resnet18(pretrained=True)
    num_ftrs = model.fc.in_features
    # 6 classes: glass, paper, cardboard, plastic, metal, trash
    model.fc = nn.Linear(num_ftrs, 6)

    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=LR, momentum=0.9)

    # Training Loop
    for epoch in range(EPOCHS):
        print(f"Epoch {epoch+1}/{EPOCHS}")

        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

            print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            wandb.log({f"{phase}_loss": epoch_loss, f"{phase}_acc": epoch_acc})

    torch.save(model.state_dict(), "models/ecovision_resnet18.pth")
    print("Training Complete. Model saved.")

if __name__ == "__main__":
    # check if data exists
    if not os.path.exists("data/raw/glass"):
        print("Data not found. Please run 'python src/data/extract_dataset.py' first.")
    else:
        train()
