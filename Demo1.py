import streamlit as st
import pandas as pd
import PyPDF2
from pathlib import Path
import subprocess
import re
import os
import torch
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
from transformers import Pix2StructForConditionalGeneration as psg
from transformers import Pix2StructProcessor as psp
from functools import partial
from time import gmtime, strftime

# Device selection
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = psg.from_pretrained("google/pix2struct-docvqa-base").to(DEVICE)
processor = psp.from_pretrained("google/pix2struct-docvqa-base")

#______________________________________________________________________________________________________________________________



def split_list_to_columns(df, column_name):
    # Get the maximum number of elements in the list
    #max_len = max(len(item) for item in df[column_name])
    
    # Create new column names based on the maximum number of elements
    #new_columns = [f'Answer_{i+1}' for i in range(max_len)]
    new_columns = ["Invoice_date", "Invoice_number", "Total"]
    
    # Create DataFrame from the split values and concatenate it with the original DataFrame
    df_split = pd.DataFrame(df[column_name].tolist(), columns=new_columns)
    df = pd.concat([df, df_split], axis=1)
    
    # Drop the original column
    df.drop(columns=[column_name], inplace=True)
    
    return df


# Function to convert PDF to images
def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images

#process_document function processes a PDF document by extracting questions and generating answers using the generate function. The generate function leverages a language model and a text processor to provide answers based on the input questions and image conten

def process_document(pdf_path, questions):
    document_data = {
        "Document Name": os.path.basename(pdf_path),
        "Questions": [],
        "Answers": [],
    }
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
        document_data["Questions"].append(question)
        document_data["Answers"].append(answer)
    return document_data


def generate(model, processor, img, questions):
    inputs = processor(
        images=[img for _ in range(len(questions))], text=questions, return_tensors="pt"
    ).to(DEVICE)
    predictions = model.generate(**inputs, max_new_tokens=256)
    return zip(questions, processor.batch_decode(predictions, skip_special_tokens=True))

#Extract data from PDF by using above two functions
def extractuploadfilesdata(uploaded_files):
    # Define the directories containing the PDF files
    invoice_directory = "./invoices"

    #Count of uploaded_files
    count_upload_files = len(uploaded_files)

    #Progress bar for file processing by model
    latest_iteration = st.empty()
    bar = st.progress(0)
    i = 0
    upload_percent = 0
    for uploaded_file in uploaded_files:
        latest_iteration.text(f"Progress: {upload_percent}%")
        invoice_path = os.path.join(invoice_directory, uploaded_file.name)
        invoice_data = process_document(
            invoice_path, questions
            )  
        # Assuming 'questions' is defined somewhere
        all_document_data.append(invoice_data)
   
        # Update the progress bar
        i += 1
        upload_percent = int((i/count_upload_files) * 100)
        latest_iteration.text(f"Progress: {upload_percent}%")
        bar.progress(upload_percent)
         #st.write("DONE for file ",uploaded_file.name)
    return all_document_data

#write data to a csv file
def writedatatofile(df,csv_file_path):
    # Write the DataFrame to the CSV file
    df.to_csv(csv_file_path, index=False)

    print(f'CSV file "{csv_file_path}" has been created successfully.')

#Fucntion combines invoice data from two CSV files, ensuring that the invoice numbers match before merging the records
def invoicesupportmatch(ipath,spath):
    idf1 =  pd.read_csv(ipath)
    idf2 = pd.read_csv(spath)
    
    idf1["Invoice_number"] = idf1["Invoice_number"].astype(str)
    idf2["Invoice_number"] = idf2["Invoice_number"].astype(str)

    #st.dataframe(idf1)
    #st.dataframe(idf2)

    #Common rows from both datarames are merged based on column Invoice_number
    mergdf = pd.merge(idf1, idf2, how='inner', on=['Invoice_number'])
    return mergdf


#PDF merger
def merge_pdfs(pdf_list, output_merge_pdf):
    merger = PyPDF2.PdfMerger()
    
    for pdf in pdf_list:
        pdf_file_path = os.path.join(csv_directory, pdf)
        merger.append(pdf_file_path)
    output_merge_path = os.path.join(csv_directory, output_merge_pdf)
    merger.write(output_merge_path)
    merger.close()
    

def viewpdf(pdf_file):
    pdf_file_path = os.path.join(csv_directory, pdf_file)
    pdf_image = convert_pdf_to_images(pdf_file_path)
    #pdf_image.resize(100, 100)
    with tab1:
        with tab1col2:
            st.image(pdf_image, use_column_width=True)

    
# _______________________________________________________________________________________________________
def main():

    #session state manage
#    if "df1" not in st.session_state:
#        st.session_state['df1'] = False
#    if "df2" not in st.session_state:
#        st.session_state['df2'] = False
#    if "matchbtn" not in st.session_state:
#        st.session_state['matchbtn'] = False
#     if "df4" not in st.session_state:
#         st.session_state['df4'] =  


    #csv_directory = "./invoices"
    invoice_extract_csv = "invoice_extract.csv"
    invoice_extract_csv_file_path = os.path.join(csv_directory, invoice_extract_csv)
   
    support_doc_extract_csv = "support_doc__extract.csv"
    support_doc_extract_csv_file_path = os.path.join(csv_directory, support_doc_extract_csv)
    
    #session state management
    if 'df1' not in st.session_state:
        st.session_state.df1 = None
    if 'df2' not in st.session_state:
        st.session_state.df2 = None

    with st.sidebar:
        #Add logo
        logo_url = "https://companieslogo.com/img/orig/CAP.PA-9b4110b0.png?t=1651902188"
        #st.image(logo_url, width=100)
        
        #Form for Invoice PDF upload 
        with st.form("form_key1"): 
            # Add a title to your app
            st.header("Upload Invoices here", divider="blue")


            # create a file uploader
            uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
            
            #copy of invoice uploaded_files 
            st.session_state.invuploaded_files = uploaded_files

            count_upload_files = len(uploaded_files)

            # Create a button labelled "Extract"
            st.header("", divider="green")

            # cature time 
            formatted_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
            for h in uploaded_files:
                st.write("Total Files Uploaded: ", count_upload_files, " at:", formatted_time)
                break

            if st.form_submit_button('EXTRACT :point_right:'):
                all_document_data_interim = extractuploadfilesdata(uploaded_files)
                
                # Create a DataFrame
                st.session_state.df1 = pd.DataFrame(all_document_data_interim)
                st.session_state.df1["Answers"] = st.session_state.df1["Answers"].apply(lambda x: x[:count] if len(x) >= count else x)
  
                # Apply the function to split the 'Answers' column
                st.session_state.df1 = split_list_to_columns(st.session_state.df1, 'Answers')
                st.session_state.df1.drop(columns=['Questions'], inplace=True)

                #write dataframe to a file Call module
                writedatatofile(st.session_state.df1,invoice_extract_csv_file_path)
        

        #Form for Support Document upload
        with st.form("form_key2"):
            # Add a title to your app
            st.header("Upload Support Document here", divider="blue")


            # create a file uploader
            uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
            count_upload_files = len(uploaded_files)

            #Copy of support document upoloaded_files
            st.session_state.supdocuploaded_files = uploaded_files

            # Create a button labelled "Extract"
            st.header("", divider="green")

            # cature time
            formatted_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
            for h in uploaded_files:
                st.write("Total Files Uploaded: ", count_upload_files, " at:", formatted_time)
                break

            if st.form_submit_button('EXTRACT :point_right:'):
                all_document_data_interim = extractuploadfilesdata(uploaded_files)
                
                # Create a DataFrame
                st.session_state.df2 = pd.DataFrame(all_document_data_interim)
                st.session_state.df2["Answers"] = st.session_state.df2["Answers"].apply(lambda x: x[:count] if len(x) >= count else x)
  
                # Apply the function to split the 'Answers' column
                st.session_state.df2 = split_list_to_columns(st.session_state.df2, 'Answers')
                st.session_state.df2.drop(columns=['Questions'], inplace=True)

                #write dataframe to a file Call module
                writedatatofile(st.session_state.df2,support_doc_extract_csv_file_path)

    
    if 'inv_button_labels' not in st.session_state:
        st.session_state.inv_button_labels = []
   
     
    st.session_state.invshowbtn = []
    st.session_state.supdocshowbtn = []
    st.session_state.mergepdfshowbtn = []
    st.session_state.mergepdfdownloadbtn = []
    with tab1:
        for invuploaded_file in st.session_state.invuploaded_files:
            #st.write(invuploaded_file.name)
            btn = 0
            st.session_state.invshowbtn.append(btn) 
            st.session_state.invshowbtn[btn] = st.button(label = f"VIEW {invuploaded_file.name}", on_click=viewpdf, args=(invuploaded_file.name,))
            btn = btn + 1
    
        for supdocuploaded_file in st.session_state.supdocuploaded_files:
            #st.write(supdocuploaded_file.name)
            btn = 0
            st.session_state.supdocshowbtn.append(btn)
            st.session_state.supdocshowbtn[btn] = st.button(label = f"VIEW {supdocuploaded_file.name}", on_click=viewpdf, args=(supdocuploaded_file.name,))
            btn = btn + 1

    with tab2:
        with st.expander("Click to expand for Invoice Data :arrow_down_small:"):
            st.dataframe(st.session_state.df1)

        with st.expander("Click to Expand for Support Document Data :arrow_down_small:"):
            st.dataframe(st.session_state.df2)

        st.session_state.matchbtn = st.button(label="MATCH INVOICE AND SUPPORTING :white_check_mark:")
        #matching the documents
        #if st.session_state['df1'] and st.session_state['df2']: 
        if st.session_state.matchbtn:
            df3 = invoicesupportmatch(invoice_extract_csv_file_path,support_doc_extract_csv_file_path)
            df3['Match'] = ['Invoice_Number'] * len(df3)
            st.session_state.df4 = df3.filter(['Document Name_x', 'Document Name_y', 'Match', 'Invoice_number'], axis=1)
            st.session_state.df4.columns = ['Invoice Document', 'Support Document', 'Match', 'Match Number'] 
            st.dataframe(st.session_state.df4)
            st.session_state.df4 = st.session_state.df4.drop(columns=['Match', 'Match Number'])


            pdffiles_lists = [list(row) for _, row in st.session_state.df4.iterrows()]
            for pdffiles_list in pdffiles_lists:
                output_merge_pdf = os.path.splitext(pdffiles_list[0])[0] + "_merged.pdf"
                merge_pdfs(pdffiles_list, output_merge_pdf)

                # Create an HTML string with custom CSS
                html_str = f"""
                <style>
                p.a {{
                font: bold 20px Courier;
                color: green;  # Change this to your desired font color
                }}
                </style>
                <p class="a">{output_merge_pdf} File Created</p>
                """

                #Show Merged File is created in html format using above code
                st.markdown(html_str, unsafe_allow_html=True)

                btn = 0
                st.session_state.mergepdfshowbtn.append(btn)
                st.session_state.mergepdfshowbtn[btn] = st.button(label = f"VIEW {output_merge_pdf}", on_click=viewpdf, args=(output_merge_pdf,))
                #btn = btn + 1

                output_merge_path = os.path.join(csv_directory, output_merge_pdf)
                # Read the existing PDF file
                with open(output_merge_path, "rb") as pdf_file:
                    pdf_content = pdf_file.read()
                st.session_state.mergepdfdownloadbtn.append(btn)
                st.session_state.mergepdfdownloadbtn[btn] = st.download_button(label=f"Download {output_merge_pdf}", data=pdf_content, file_name="newpdf.pdf", mime="application/pdf")
                btn = btn + 1    
            
    #    elif st.session_state.matchbtn:
    #        st.write(":point_left: Please Upload both Invoice and Support Documents to Match")

    
    

 
if __name__ == "__main__":

    # Add custom CSS for the button size
    css = """
    <style>
        button {
            height: auto;  # Set the desired height
            width: auto;  # Set the desired width
            color: blue;  # Change the button color if needed
            font-size: 50px;  # Set the desired font size
            padding-top: 10px !important;
            padding-bottom: 10px !important;
        }
    </style>
    """


    # Create an HTML string with custom CSS
    heading_str = f"""
    <style>
        .centered-text {{
            text-align: center;
            font: bold 40px Courier;
            color: blue;  /* Change this to your desired font color */
        }}
    </style>
    <p class="centered-text">DocGenAI</p>
    """

    # Show the centered heading
    st.markdown(heading_str, unsafe_allow_html=True)

    
    # Apply the CSS using st.markdown
    st.markdown(css, unsafe_allow_html=True)

    # Define the list of questions
    
    csv_directory = "./invoices"
    questions = [
        "What is the Invoice Date or Bill date",
        "What is the Invoice No.?",
        "What is the Total or Balance or Final cost ?",
        ]
    count = len(questions)

    # Initialize lists to store document names, questions, and answers
    all_document_data = []
    
    #Define Layout
    if st.button('Refresh Page'):
        st.experimental_rerun()
    tab1, tab2 = st.tabs(["UPLOADED FILES", "UPLOADED FILES EXTRACT"])
    tab1col1, tab1col2 = st.columns(2)
    main()
