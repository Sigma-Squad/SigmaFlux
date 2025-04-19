import streamlit as st
import pandas as pd
import numpy as np
import cv2
import os

# Page configuration
st.set_page_config(page_title="Digital Attendance Upload", page_icon="📋", layout="wide")
imagepath="insti1.jpeg"
if os.path.exists(imagepath):
    print('path exists')
    # Background Image
    st.markdown(
        """
        <style>
            body {
                background-image: url('https://www.instagram.com/sigmasquad_iitt/?utm_source=qr&igsh=MnRzMmM2dXFqNmh4#'); 
                background-size: cover; 
                background-repeat: no-repeat; 
                background-attachment: fixed; 
                background-position: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.error("path doesn't exist")

# Title and Description
st.markdown(
    """
    <h1 style='text-align: center; color: #4B8BBE;'>📥 Digital Attendance Upload</h1>
    <p style='text-align: center; color: #6B7280; font-size: 18px;'>Upload your Attendance sheet Image for quick processing.</p>

    <style>
        .stApp {
            background-color: #000000;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# File uploader
st.markdown(
    """
    <hr>
    <p style='position: absolute; top: 100px; right: 25%; font-size: 40px; color: #000000; z-index: 999 ; '>Choose an Image file for attendance processing</p>
    """,
    unsafe_allow_html=True
)
uploaded_file = st.file_uploader("Choose an Image file", type=["png","jpg","jpeg"], label_visibility="hidden")
if "show_links" not in st.session_state:
    st.session_state["show_links"] = True
if "show_image" not in st.session_state:
    st.session_state["show_image"]=False
# Handling file upload
if uploaded_file is not None:
    try:
        # Reading the uploaded Image file
        byte_file=np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image=cv2.imdecode(byte_file,cv2.IMREAD_COLOR) 
        # Display/Hide the image
        if st.button('View/Hide the Image'):
            st.session_state["show_image"]=not st.session_state["show_image"]
            st.session_state["show_links"] = not st.session_state["show_links"]

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
if st.session_state['show_links']:
    st.markdown(
    """
    <div>
        <a href='https://www.instagram.com/sigmasquad_iitt/?utm_source=qr&igsh=MnRzMmM2dXFqNmh4#' target='_blank'
           style='
               position: fixed;
               top: 95%;
               right: 1%;
               font-size: 20px;
               color: #1f77b4;
               text-decoration: none;
               z-index: 999;
           '>
           <img src='https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png' alt='Logo' width='20'>
            Follow us on Instagram
        </a>
    </div>
    <div>
        <a href='https://www.linkedin.com/company/sigma-squad-an-iit-tirupati-ai-ml-club/' target='_blank'
           style='
               position: fixed;
               top: 95%;
               right: 47%;
               font-size: 20px;
               color: #1f77b4;
               text-decoration: none;
               z-index: 999;
           '>
           <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' alt='Logo' width='20'>
            Visit us on Linked-In
        </a>
    </div>
    <div>
        <a href='https://github.com/Sigma-Squad' target='_blank'
           style='
               position: fixed;
               top: 95%;
               left: 1%;
               font-size: 20px;
               color: #1f77b4;
               text-decoration: none;
               z-index: 999;
           '>
           <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' alt='Logo' width='20'>
            Look out on Github
        </a>
    </div>
""",
    unsafe_allow_html=True
)

if not st.session_state['show_links']:
    st.markdown(
    """
    <div>
        <a href='https://www.instagram.com/sigmasquad_iitt/?utm_source=qr&igsh=MnRzMmM2dXFqNmh4#' target='_blank'
           style='
               position: absolute;
               top: 2200px;
               right:-50px;
               font-size: 20px;
               color: #1f77b4;
               text-decoration: none;
               z-index: 999;
           '>
           <img src='https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png' alt='Logo' width='20'>
            Follow us on Instagram
        </a>
    </div>
    <div>
        <a href='https://www.linkedin.com/company/sigma-squad-an-iit-tirupati-ai-ml-club/' target='_blank'
           style='
               position: absolute;
               top: 2200px;
               right:700px;
               font-size: 20px;
               color: #1f77b4;
               text-decoration: none;
               z-index: 999;
           '>
           <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' alt='Logo' width='20'>
            Visit us on Linked-In
        </a>
    </div>
    <div>
        <a href='https://github.com/Sigma-Squad' target='_blank'
           style='
               position: absolute;
               top: 2200px;
               left:-50px;
               font-size: 20px;
               color: #1f77b4;
               text-decoration: none;
               z-index: 999;
           '>
           <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' alt='Logo' width='20'>
            Look out on Github
        </a>
    </div>
""",
    unsafe_allow_html=True
)

if st.session_state["show_image"]:
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Uploaded Image", use_container_width=True)

st.markdown(
    """
    <hr>
    <p style='position: absolute; top: 100px; right: 700px; color: #9CA3AF;'>Developed by SigmaSquad</p>
    """,
    unsafe_allow_html=True
)
