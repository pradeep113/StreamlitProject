import streamlit as st
from pathlib import Path

#*****Function to read pdf invlices and extract its data and writes on a csv file.*****
def pdf_text_extract(uploaded_file):
  st.text("File name is : uploaded_file")

def main():
  # Add a title to your app
  st.title("Upload Invoices here")

  #Define the desired path
  path = "/Users/pradeepkumar/Pictures/uploaded_files"
  file_path = Path(path)

  #create a file uploader
  uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
  st.text("Files uploaded")
  if uploaded_files:
        for uploaded_file in uploaded_files:
            # Read the uploaded file (assuming CSV format)
            #dataframe = pd.read_csv(uploaded_file)
            st.write("File name:", uploaded_file.name)
            #st.write(dataframe)  # Display the data (you can customize this part)
            #Create button for each file
            if st.button("Extract : {uploaded_file.name}"):
               pdf_text_extract({uploaded_file.name})
            
              
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
