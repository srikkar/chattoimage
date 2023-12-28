import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
print('Loading .env file')

import os
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
genai.temperature = 0  # Adjust between 0 (more deterministic) and 1 (more random)
# Set page config
st.set_page_config(
    page_title="Talk to Image",
    initial_sidebar_state="expanded",
)

# Set theme
st.markdown("""
    <style>
        .reportview-container {
            background: #273346;  # Change the color according to your theme
        }
        .sidebar .sidebar-content {
            background: #B9F1C0;  # Change the color according to your theme
        }
    </style>
""", unsafe_allow_html=True)

# Add title to the header section
st.title("Talk to Image")  # Add your title here

uploaded_file = st.file_uploader("Upload your image here", type=['png', 'jpg', 'jpeg'])
model = genai.GenerativeModel('gemini-pro-vision')
image = None

def get_gemini_response(image, input):
    try:
        with st.spinner('Analyzing Image...'):
            response = model.generate_content(["Analyse the image and answer to the Questions based on the image. Do not give any extra content outisde the Image Provided. Is the Answer is not found from the context provided, say, I'm sorry, I dont see the answer from the Image.", image, input])
            response.resolve()
            return response.text
    except Exception as eor:
        print(eor)
        return "Error Occurred"

if uploaded_file is not None:
    with st.spinner('Uploading Image...'):
        # Open the image file
        image = Image.open(uploaded_file)
        # Display the image
        st.image(image, caption='Uploaded Image', use_column_width=True)

    with st.spinner('Analyzing the Image...'):
        input = st.text_input("Ask Something about the Image: ", key="input")

submit = st.button("Ask")
if submit:
    st.subheader("Answer is...")
    response = get_gemini_response(image, input)
    st.write(response)
