import streamlit as st
import pandas as pd
import PyPDF2
from pathlib import Path




#***Function to read all pdf invlices and extract its data and writes on csv file.***
def all_pdf_text_extract(uploaded_files):
  st.write("Files Uploaded are :")
  for each_file in uploaded_files:
      st.write(each_file.name)
  
  
#*****Function to read pdf invoices and extract its data and writes on a csv file.*****
def pdf_text_extract(uploaded_file, output_csv):
  st.text(f"File name is : {uploaded_file.name}")
  pdf_file = uploaded_file
  #with open(pdf_path, 'rb') as pdf_file:
  pdf_reader = PyPDF2.PdfReader(pdf_file)
  text = ''
  for page in pdf_reader.pages:
        text += page.extract_text() + '\n'

  # Extract the desired lines (modify as needed)
  selected_lines = [line for line in text.split('\n') if line.startswith("Total Due") or line.startswith("Invoice Date")] 
  df = pd.DataFrame({'Text': [selected_lines]})
  df.to_csv(output_csv, index=False)
  st.write(selected_lines)
  if selected_line:
    st.download_button("Download Ouput.csv file", str(selected_lines[0]))


def main():
  # Add a title to your app
  st.header("Upload Invoices here", divider='blue')

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
            #dataframe = pd.read_csv(uploaded_file)
            st.write(f"File name:", uploaded_file.name, "uploaded")
            #st.write(dataframe)  # Display the data (you can customize this part)
            #Create button for each file
            if st.button(f"Extract : {uploaded_file.name}"):
               pdf_text_extract(uploaded_file, output_csv)
            
              
  #Create a button labelled "Extract"
  st.header("",divider='green')
  if st.button("EXTRACT", key="Extract"):
    all_pdf_text_extract(uploaded_files)


    
  # Create a slider widget to select a value
  #selected_value = st.slider("Select a value", 0, 100)

  # Calculate the square of the selected value
  #squared_value = selected_value * selected_value

  # Display the result
  #st.write(f"{selected_value} squared is {squared_value}")

  # Run the app using the following command:
  #   streamlit run your_file_name.py

if __name__ == "__main__":
  main()
