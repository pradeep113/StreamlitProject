import streamlit as st

# Add a title to your app
st.title("My First Streamlit App")

# Create a slider widget to select a value
selected_value = st.slider("Select a value", 0, 100)

# Calculate the square of the selected value
squared_value = selected_value * selected_value

# Display the result
st.write(f"{selected_value} squared is {squared_value}")

# Run the app using the following command:
# streamlit run your_file_name.py
