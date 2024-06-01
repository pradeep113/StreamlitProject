
import streamlit as st
import pandas as pd
import PyPDF2
from pathlib import Path
import subprocess
import re
from pdf2image import convert_from_path, convert_from_bytes
from transformers import Pix2StructForConditionalGeneration as psg
from transformers import Pix2StructProcessor as psp
from functools import partial

#_____________________________________________________________________________________________________
#***Function to read all pdf invlices and extract its data and writes on csv file.***
def all_pdf_text_extract(uploaded_files):
  st.write("Files Uploaded are :")
  for each_file in uploaded_files:
      st.write(each_file.name)
  
  
#*****Function to read pdf invoices and extract its data and writes on a csv file.*****
def pdf_text_extract(uploaded_file, output_csv):
  st.text(f"File name is : {uploaded_file.name}")
  pdf_file = uploaded_file
  pdf_reader = PyPDF2.PdfReader(pdf_file)
  text = ''
  for page in pdf_reader.pages:
        text += '\n' +page.extract_text() + '\n'
 
  st.write(text)

  # Extract the desired lines (modify as needed)
  selected_lines = [line for line in text.split('\n') if line.startswith("Invoice Number") or line.startswith("Total Due") or line.startswith("Invoice Date")] 
  
  #df = pd.DataFrame({'Text': [selected_lines]})
  #df.to_csv(output_csv, index=False)
  st.write(selected_lines)
  #if selected_line is not none:
  st.download_button("Download Ouput file", str(selected_lines))

  #ocrmypdf.ocr(pdf_file, 'put.pdf', skip_text=True)
  #print('File converted successfully!')
#_________________________________________________________________________________________________________
# Function to convert PDF to images
def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images

def process_document(pdf_path, questions):
    document_data = {'Document Name': os.path.basename(pdf_path), 'Questions': [], 'Answers': []}
    # Convert PDF to images
    document_images = convert_pdf_to_images(pdf_path)
    # Generate completions for document
    generator = partial(generate, model, processor)
    completions = []
    for image in document_images:
        completions.extend(generator(image, questions))
    # Store questions and answers
    for completion in completions:
        question, answer = completion
        document_data['Questions'].append(question)
        document_data['Answers'].append(answer)
    return document_data

def generate(model, processor, img, questions):
    inputs = processor(images=[img for _ in range(len(questions))], text=questions, return_tensors="pt").to(DEVICE)
    predictions = model.generate(**inputs, max_new_tokens=256)
    return zip(questions, processor.batch_decode(predictions, skip_special_tokens=True))

#_______________________________________________________________________________________________________
def main():
  
  # Add a title to your app
  st.header("Upload Invoices here", divider='blue')

  #Define the desired path
  #path = "/Users/pradeepkumar/Pictures/uploaded_files"
  #file_path = Path(path)

  #files to create 
  output_csv = 'output.csv'

  #create a file uploader
  uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

  st.header("",divider='blue')
  
  # Define the directories containing the PDF files
  invoice_directory = "./invoices"

  # Define the list of questions
  questions = ["What is the B/L Number?", "What is the TO Number ?", "What is the Invoice No.?", "What is the container No.?"]
  count = len(questions)
  count


  # Initialize lists to store document names, questions, and answers
  all_document_data = []

  # Function to convert PDF to images
  def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images

  # Device selection
  DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
  model = psg.from_pretrained("google/pix2struct-docvqa-base").to(DEVICE)
  processor = psp.from_pretrained("google/pix2struct-docvqa-base")



  if uploaded_files:
        for uploaded_file in uploaded_files:
            # Read the uploaded file (assuming CSV format)
            st.write(f"File name:", uploaded_file.name, "uploaded")
            #st.write(f"at:", {uploaded_file.uploaded_at})
            #Create button for each file
            if st.button(f"Extract : {uploaded_file.name}"):
               pdf_text_extract(uploaded_file, output_csv)

                      

  
  #Create a button labelled "Extract"
  st.header("",divider='green')
  if st.button("EXTRACT", key="Extract"):
    if uploaded_files:
      for uploaded_file in uploaded_files:
        invoice_path = os.path.join(invoice_directory, uploaded_file.name)
        invoice_data = process_document(invoice_path, questions)  # Assuming 'questions' is defined somewhere
        all_document_data.append(invoice_data)


     
  # Run the app using the following command:
  #   streamlit run your_file_name.py

if __name__ == "__main__":
  main()