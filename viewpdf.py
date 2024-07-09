import os
from PIL import Image
import streamlit as st
import io
from pdf2image import convert_from_path

pdf_saved_path = "C:\\Python\\StreamlitProject1\\invoice_upload\\"

def save_uploaded_file(uploaded_file):
    # Create a folder named 'uploaded_files' if it doesn't exist
    os.makedirs(pdf_saved_path, exist_ok=True)
    # Save the uploaded PDF file to the 'uploaded_files' folder
    with open(os.path.join(pdf_saved_path, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

def convert_pdf_to_image(pdf_path):
    # Convert the first page of the PDF to an image
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    return images[0]

st.title('PDF File Upload')
uploaded_files = st.file_uploader("Upload PDF", type='pdf', accept_multiple_files=True)
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        save_uploaded_file(uploaded_file)

pdf_files = [os.path.join(pdf_saved_path, f) for f in os.listdir(pdf_saved_path) if f.endswith('.pdf')]

if not pdf_files:
    st.write("No PDF files found in the specified directory.")
else:
    st.write(f"Found {len(pdf_files)} PDF files.")
    st.write("### Preview of First Pages:")

    for pdf_file in pdf_files:
        try:
            # Convert PDF to image
            first_page_image = convert_pdf_to_image(pdf_file)
            first_page_image.resize((100, 100))
            # Display the image
            st.image(first_page_image, caption=os.path.basename(pdf_file), use_column_width=True)
        except Exception as e:
            st.write(f"Error processing file {pdf_file}: {e}")
