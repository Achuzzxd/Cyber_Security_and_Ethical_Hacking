import streamlit as st

st.set_page_config(page_title="Payment Page", layout="centered")
st.title("💳 Payment Portal")

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

    .password-box {
        background-color: #111111;
        color: #00FFFF;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 18px;
        display: inline-block;
        margin-top: 10px;
        margin-bottom: 20px;
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

source = st.session_state.get("source", "Unknown")
st.markdown(f"<h3>Payment for: <strong>{source}</strong></h3>", unsafe_allow_html=True)

if source == "Decrypt_files":
    string1 = st.text_input("Enter transaction address")
    if st.button("Pay now"):
        if not string1:
            st.warning("Please enter the transaction address.")
        elif string1 == "#gj236gbbjw88290sbbjsjd37yew8wbssu38eddkkn":
            st.success(f"✅ Payment successful for **{source}**.")
            st.markdown("""
            <p>Copy the password and use them to decrypt</p>
            <h3>Password for Decrypting your Files:</h3>
            <div class='password-box'>Yourdecryption</div>
            """, unsafe_allow_html=True)
        else:
            st.warning("❌ Incorrect address")
        st.page_link("pages/Decrypt_files.py", label="Go back")

elif source == "Decrypt_folder":
    string1 = st.text_input("Enter transaction address")
    if st.button("Pay now"):
        if not string1:
            st.warning("Please enter the transaction address.")
        elif string1 == "#gj236gbbjw88290sbbjsjd37yew8wbssu38eddkkn":
            st.success(f"✅ Payment successful for **{source}**.")
            st.markdown("""
            <p>Copy the password and use them to decrypt</p>
            <h3>Password for Decrypting your Folder:</h3>
            <div class='password-box'>Decryptyourfolder</div>
            """, unsafe_allow_html=True)
        else:
            st.warning("❌ Incorrect address")
    st.page_link("pages/Decrypt_folder.py", label="Go back")

elif source == "Decrypt_folders_and_files":
    string1 = st.text_input("Enter transaction address")
    if st.button("Pay now"):
        if not string1:
            st.warning("Please enter the transaction address.")
        elif string1 == "#gj236gbbjw88290sbbjsjd37yew8wbssu38eddkkn":
            st.success(f"✅ Payment successful for **{source}**.")
            st.markdown("""
            <p>Copy the password and use them to decrypt</p>
            <h3>Password for Decrypting your Folders and Files:</h3>
            <div class='password-box'>FilesareDecrypted</div>
            """, unsafe_allow_html=True)
        else:
            st.warning("❌ Incorrect address")
    st.page_link("pages/Decrypt_folders_and_files.py", label="Go back")

else:
    st.write("⚠️ Unknown source. Please go back and try again.")
