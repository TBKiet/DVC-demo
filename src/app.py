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

    # Placeholder for prediction
    classes = ['glass', 'paper', 'cardboard', 'plastic', 'metal', 'trash']

    # Preprocessing
    # transform = ...
    # input_tensor = ...

    # Model inference
    # output = model(input_tensor)
    # _, predicted = torch.max(output, 1)

    # st.write(f"Prediction: **{classes[predicted.item()]}**")
    st.info("Model not yet trained. Please train the model first.")
