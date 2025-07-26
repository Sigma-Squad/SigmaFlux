import streamlit as st
import pandas as pd
import numpy as np
import cv2
import os
import io
import time

# Assume the processing functions are available (either directly in this file or imported)
import SigmaFlux

# Page configuration
st.set_page_config(page_title="Digital Attendance Upload", page_icon="📋", layout="wide")
api_key=st.secrets['api-key']

# Define the color palette based on the Sigma Squad GitHub logo
background_color = "#0D1B2A"  # Dark Blue/Almost Black
primary_color = "#00FFFF"     # Electric Blue (approximated from logo)
text_color = "#FFFFFF"       # White

custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&family=Lato:wght@400;700&display=swap');

html, body, .stApp {{
    background-color: {background_color} !important;
    color: {text_color} !important;
    font-family: 'Open Sans', sans-serif;
    line-height: 1.6;
    font-size: 16px;
}}

* {{
    color: {text_color} !important;
    background-color: transparent !important;
    border-color: {primary_color} !important;
}}

h1, h2, h3 {{
    color: {primary_color} !important;
    font-family: 'Lato', sans-serif;
    text-shadow: 1px 1px 4px #000000;
    margin-bottom: 10px;
}}

.stMarkdown, .stFileUploader, .stNumberInput, .stButton {{
    margin-bottom: 1.5rem !important;
}}

.stButton>button {{
    background-color: {primary_color} !important;
    color: {background_color} !important;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    border: none !important;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    box-shadow: 0px 4px 10px rgba(0,255,255,0.3);
}}

.stButton>button:hover {{
    background-color: {text_color} !important;
    color: {background_color} !important;
    transform: scale(1.02);
}}

.stFileUploader label {{
    font-family: 'Lato', sans-serif;
    font-size: 18px;
    margin-bottom: 8px;
    display: block;
    color: {primary_color} !important;
}}

.stFileUploader div[data-testid="stFileUploaderDropzone"] {{
    background-color: #1A1A2E !important;
    border: 2px dashed {primary_color} !important;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    transition: border-color 0.3s ease-in-out, background-color 0.3s ease-in-out;
}}

.stFileUploader div[data-testid="stFileUploaderDropzone"]:hover {{
    border-color: {text_color} !important;
    background-color: #222244 !important;
}}

div[data-testid="stMarkdown"] div {{
    background-color: #1A1A2E !important;
    color: {text_color} !important;
    border-left: 5px solid {primary_color};
    padding: 15px;
    margin-bottom: 24px;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 255, 255, 0.1);
}}

.stImage caption {{
    text-align: center;
    font-style: italic;
    margin-top: 8px;
    font-size: 14px;
}}

input, select {{
    background-color: #1A1A2E !important;
    color: {text_color} !important;
    border: 1px solid {primary_color} !important;
    padding: 10px;
    border-radius: 5px;
    font-family: 'Open Sans', sans-serif;
}}

hr {{
    border: none;
    border-top: 1px solid {primary_color};
    margin: 2rem 0;
}}

div a {{
    color: {text_color} !important;
    text-decoration: none;
    font-weight: 500;
    margin-right: 20px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: color 0.2s ease;
}}

div a:hover {{
    color: {primary_color} !important;
    text-decoration: underline;
}}

footer {{
    margin-top: 3rem;
    text-align: center;
}}

</style>
"""

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Title and Description
st.markdown(
    """
    <h1 style='text-align: center;'>📥 Digital Attendance Upload</h1>
    <p style='text-align: center;'>Upload your Attendance sheet Image for quick processing.</p>
    """,
    unsafe_allow_html=True
)

# File uploader section
st.markdown(
    """
    <hr>
    """,
    unsafe_allow_html=True
)

# Stylish message about input format
st.markdown(
    """
    <div>
        <p>⬆️ Please upload an image in <strong>PNG, JPG, or JPEG</strong> format.</p>
    </div>
    """,
    unsafe_allow_html=True
)


# Stylish message about download format
st.markdown(
    """
    <div>
        <p>✅ Your processed attendance sheet will be downloaded in <strong>.xlsx</strong> format.</p>
    </div>
    """,
    unsafe_allow_html=True
)


uploaded_file = st.file_uploader("Choose an Image file", type=["png","jpg","jpeg"], label_visibility="hidden")

if uploaded_file is not None:
    st.success("Image uploaded successfully!")
    try:
        byte_file = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(byte_file, cv2.IMREAD_COLOR)

        if 'show_image' not in st.session_state:
            st.session_state['show_image'] = False

        if st.button('View/Hide the Image'):
            st.session_state['show_image'] = not st.session_state['show_image']

        if st.session_state['show_image']:
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Uploaded Image", use_container_width=True)

        # Add input for number of days with clearer label
        num_days = st.number_input("Enter the number of attendance days recorded in the image:", min_value=1, value=1, step=1)
        st.info("Please enter the exact number of days the attendance sheet covers.")

        # Add a process button
        if st.button("Process Attendance"):
            if num_days > 0:
                # Add a loading spinner
                with st.spinner("Processing image... This may take a moment."):
                    # Simulate processing time (replace with actual function calls)
                    # time.sleep(3) # Simulate image processing

                    # Placeholder for calling processing functions
                    try:
                        final_excel_data = SigmaFlux.main(image, uploaded_file.name, num_days,api_key)
                        st.success("Processing complete!")

                        # --- Start of Download Button Logic ---
                        # Assuming final_excel_data is a pandas DataFrame
                        # Create an in-memory Excel file
                        excel_buffer = io.BytesIO()
                        final_excel_data.to_excel(excel_buffer, index=False)
                        excel_buffer.seek(0) # Reset buffer position to the beginning

                        # Get the base name of the uploaded file (without extension)
                        file_name_base = os.path.splitext(uploaded_file.name)[0]
                        download_file_name = f"{file_name_base}_attendance_data.xlsx"

                        # Create the download button
                        st.download_button(
                            label="Download Attendance Data",
                            data=excel_buffer,
                            file_name=download_file_name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        # --- End of Download Button Logic ---

                    except Exception as e:
                        st.error(f"An error occurred during processing: {e}")


            else:
                st.warning("Please enter a valid number of days (greater than 0).")

    except Exception as ex:
        st.error(f"❌ Error processing file: {ex}")

# Footer links will always be displayed below the image or other content
st.markdown("""
    <div>
        <a href='https://www.instagram.com/sigmasquad_iitt/?utm_source=qr&igsh=MnRzMmM2dXFqNmh4#' target='_blank'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png' width='20'> Follow us on Instagram</a>
        &nbsp;&nbsp;&nbsp;
        <a href='https://www.linkedin.com/company/sigma-squad-an-iit-tirupati-ai-ml-club/' target='_blank'>
        <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='20'> Visit us on LinkedIn</a>
        &nbsp;&nbsp;&nbsp;
        <a href='https://github.com/Sigma-Squad' target='_blank'>
        <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' width='20'> Look out on GitHub</a>
    </div>
""", unsafe_allow_html=True)


st.markdown(
    f"""
    <div style='text-align: center; margin-top: 50px; color: {primary_color}; font-family: "Open Sans", sans-serif;'>
        Developed by SigmaSquad
    </div>
    """,
    unsafe_allow_html=True
)
