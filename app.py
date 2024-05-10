# Q&A Chatbot
#from langchain.llms import OpenAI

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyA4TYAwPLjUFA-pyVaGnVlP9x051jRLGgI"

genai.configure(api_key=GOOGLE_API_KEY)

input_prompt = """
               You are an expert in creating detailed plans for achieving goals on the basis of provided deadline and capabilities of the individual.
               You will receive input image of a syllabus, users capabilities in terms of text and a deadline alongwith how much time they can commit per day.
               Generate a detailed personalized plan on the basis of all this information so that the user can achieve their goal efficiently and effectively in the given time frame.
               The plan should define which topic should be done when and how much time should be spent on each topic. You should account for the complexity of the topics and make the plan accordinly.
               """
## Function to load OpenAI model and get respones

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    result=response.text
    # result = result[0]['text']
    return result
    

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Set the page configuration
st.set_page_config(page_title="Code Generator", page_icon=":guardsman:", layout="wide")

# Initialize the app
header = st.container()
with header:
    st.markdown("<h1 style='text-align: center; font-size: 40px; padding: 20px 0;'>Personalized Plan Generator</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    deadline = st.number_input("Deadline (in days):", min_value=1, value=1, step=1, format="%d")
    hours = st.number_input("Hours per day:", min_value=1, value=1, step=1, format="%d")

with col2:
    caps = st.text_area("Enter your capabilities:")

uploaded_file = st.file_uploader("Upload syllabus image:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded syllabus image.", use_column_width=True)

# Generate the plan
submit = st.button("Generate plan", key="generate_plan_btn")
input = "The deadline is {deadline} days and the user can commit {hours} hours per day. The user's capabilites are {caps}.".format(deadline=deadline, hours=hours, caps=caps)
if submit:
    with st.spinner("Generating plan..."):
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input)
        st.subheader("The detailed plan is")
        st.write(response)