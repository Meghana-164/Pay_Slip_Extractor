import streamlit as st
import pandas as pd
from utils.ocr_utils import process_document
from utils.llm_extraction import extract_fields_from_text
import os

st.set_page_config(page_title="KYC Extractor - Gemini", layout="centered")
st.title("📑 Gemini-based KYC Extractor")
st.subheader("Upload one or more KYC documents (PDF or Image formats)")

uploaded_files = st.file_uploader(
    "📤 Upload KYC Document(s)",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Default form fields
form_fields = {
    "Name": "",
    "Father's Name": "",
    "Occupation": "",
    "Amount": "",
    "Address": "",
    "Company Name": "",
    "PAN ID": "",
    "Aadhar ID": ""
}

# Make sure extracted_data folder exists
os.makedirs("extracted_data", exist_ok=True)

# Manual trigger to process files
if uploaded_files:
    if st.button("🔍 Extract Details from Uploaded Files"):
        combined_text = ""
        for file in uploaded_files:
            with st.spinner(f"Processing {file.name}..."):
                try:
                    doc_text = process_document(file)
                    combined_text += doc_text + "\n"
                except Exception as e:
                    st.error(f"❌ Could not process {file.name}: {e}")

        if combined_text.strip():
            extracted = extract_fields_from_text(combined_text)
            if "error" in extracted:
                st.error(extracted["error"])
            else:
                for k in form_fields:
                    if k in extracted and extracted[k]:
                        form_fields[k] = extracted[k]

# KYC editable form
with st.form("kyc_form"):
    st.markdown("### ✍️ Review / Edit Extracted KYC Details")

    form_fields["Name"] = st.text_input("Name", value=form_fields["Name"])
    form_fields["Father's Name"] = st.text_input("Father's Name", value=form_fields["Father's Name"])
    form_fields["Occupation"] = st.text_input("Occupation", value=form_fields["Occupation"])
    form_fields["Amount"] = st.text_input("Amount", value=form_fields["Amount"])
    form_fields["Address"] = st.text_area("Address", value=form_fields["Address"])
    form_fields["Company Name"] = st.text_input("Company Name", value=form_fields["Company Name"])
    form_fields["PAN ID"] = st.text_input("PAN ID", value=form_fields["PAN ID"])
    form_fields["Aadhar ID"] = st.text_input("Aadhar ID", value=form_fields["Aadhar ID"])

    submitted = st.form_submit_button("💾 Save KYC Info")

    if submitted:
        df = pd.DataFrame([form_fields])
        df.to_csv("extracted_data/kyc_user_data.csv", index=False)
        st.success("✅ Data saved to extracted_data/kyc_user_data.csv")
        st.download_button("⬇️ Download CSV", data=df.to_csv(index=False), file_name="kyc_output.csv", mime="text/csv")
