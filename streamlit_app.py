import streamlit as st
import pandas as pd
import PyPDF2
from pathlib import Path
import subprocess
import re





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



def main():
  
  # Add a title to your app
  st.header("Upload Invoices Files here", divider='blue')

  #Define the desired path
  path = "/Users/pradeepkumar/Pictures/uploaded_files"
  file_path = Path(path)

  #files to create 
  output_csv = 'output.csv'

  #create a file uploader
  uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

  st.header("",divider='blue')
  
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
    all_pdf_text_extract(uploaded_files)

    
 
  # Run the app using the following command:
  #   streamlit run your_file_name.py

if __name__ == "__main__":
  main()
