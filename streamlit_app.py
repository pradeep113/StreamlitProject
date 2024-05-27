import streamlit as st
from pathlib import Path

#*****Function to read pdf invlices and extract its data and writes on a csv file.*****
def pdf_text_extract():
  print("Script executed")

def main():
  # Add a title to your app
  st.title("Upload Invoices here")

  #Define the desired path
  path = "/Users/pradeepkumar/Pictures/uploaded_files"
  file_path = Path(path)

  #create a file uploader
  uploaded_file = st.file_uploader("Pick a file")
  st.text("Files uploaded")

  #Create a button labelled "Extract"
  if st.button("extract", key="Extract"):
    pdf_text_extract()
    
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
