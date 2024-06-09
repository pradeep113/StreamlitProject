import streamlit as st
import pandas as pd
from transformers import pipeline
import math


#calling Model from hugging face
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

#Sets up the Streamlit sidebar with input options for text, image, and a button to generate a response.

with st.sidebar:
    logo_url = "https://companieslogo.com/img/orig/CAP.PA-9b4110b0.png?t=1651902188"
    st.header("Text a Complain")
    text_input_prompt = st.text_input("Enter Complain prompt: ", key="input")
    st.markdown("<h1 style='text-align: center;'>(or)</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Complaint File", type=["xlsx"])
    submit = st.button("SUMMARIZE")
st.title("Complaint Summarizer")
#Checks user input and triggers the generation of a response based on either text input or an uploaded image.

if submit:
    if uploaded_file is not None:    
        df = pd.read_excel(uploaded_file, skiprows=1)
        df = df.iloc[:, 1:]

        # Convert DataFrame to a list of sentences
        data = df.to_string(index=False, header=False).split('\n')

        for sentence in data:
            sentence = sentence.strip()
            min_length = int(0.1 * len(sentence))
            max_length = math.floor(0.25 * len(sentence))
            if len(sentence.split()) > 5:
                summ = summarizer(sentence, max_length=max_length, min_length=min_length, do_sample=False)
 
            if summ:  # Check if the list is not empty
                st.header(" ",divider="blue")
                st.write(f"Complain: ",sentence)
                st.write(f"Summary: {summ[0]['summary_text']}")
                st.header(" ",divider="green")
            else:
                st.write("No summary available for this sentence.")
    elif text_input_prompt is not None:
        with st.spinner("Summarizing..."): 
            min_length = int(0.1 * len(text_input_prompt))
            max_length = math.floor(0.25 * len(text_input_prompt))
            summ = summarizer(text_input_prompt, max_length=max_length, min_length=min_length, do_sample=False)
 
            if summ:  # Check if the list is not empty
                st.header(" ",divider="blue")
                st.write(f"Complain: ",text_input_prompt)
                st.write(f"Summary: {summ[0]['summary_text']}")
                st.header(" ",divider="green")
            else:
                st.write("No summary available for this sentence.")
        #st .subheader("Generated Summary:")





    #logo_url = "https://companieslogo.com/img/orig/CAP.PA-9b4110b0.png?t=1651902188"
    #st.image(logo_url, width=100)

    
    # Add a title to your app
    #st.header("Upload Invoices here", divider="blue")
