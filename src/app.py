import streamlit as st
import torch
import torchvision.transforms as transforms
from PIL import Image
import os
# import model definition here

st.set_page_config(page_title="EcoVision - specific waste sorting", page_icon="♻️")

st.title("♻️ EcoVision: Waste Classification")
st.write("Upload an image of waste (Glass, Paper, Cardboard, Plastic, Metal, Trash) to classify it.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    st.write("Classifying...")

    # Define classes (Sorted alphabetically as per ImageFolder default)
    classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

    # Load Model
    device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    model_path = "models/ecovision_resnet18.pth"

    if os.path.exists(model_path):
        # Recreate the model structure
        from torchvision import models
        import torch.nn as nn

        model = models.resnet18(pretrained=False) # No need for pretrained weights, we load ours
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, 6)

        # Load state dict
        try:
            model.load_state_dict(torch.load(model_path, map_location=device))
            model.to(device)
            model.eval()

            # Preprocessing
            transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])

            # Inference
            if image.mode != 'RGB':
                image = image.convert('RGB')

            input_tensor = transform(image).unsqueeze(0).to(device)

            with torch.no_grad():
                output = model(input_tensor)
                probabilities = torch.nn.functional.softmax(output[0], dim=0)

            # Get top prediction
            top_prob, top_catid = torch.topk(probabilities, 1)
            predicted_label = classes[top_catid.item()]
            confidence = top_prob.item() * 100

            st.success(f"Prediction: **{predicted_label.title()}** ({confidence:.2f}%)")

            # Show probability bar chart
            st.bar_chart({c: p.item() for c, p in zip(classes, probabilities)})

        except Exception as e:
            st.error(f"Error loading model: {e}")
    else:
        st.warning("Model file not found. Please train the model first by running `python src/train.py`.")
