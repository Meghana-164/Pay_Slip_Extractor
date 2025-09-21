# 📑 KYC Auto-Fill System (Streamlit + OCR + LLM)

This project automates the extraction of user details from KYC documents (Aadhaar, PAN, Payslips, etc.) and auto-fills them into a structured form.  
It combines **OCR (Optical Character Recognition)** with **Large Language Models (LLMs)** to achieve accurate field extraction.

---

## 🚀 Features
- Upload multiple **PDFs or images** (Aadhaar, PAN, Payslip, etc.)
- Extracts key details like:
  - Name  
  - Father’s Name  
  - Occupation  
  - Amount  
  - Address  
  - Company Name  
  - PAN ID  
  - Aadhar ID  
- **Auto-populates** extracted details into a Streamlit form
- Users can **edit before saving**
- Export extracted data to **CSV** for downstream use

---

## 🛠️ Tech Stack
- **Frontend/UI:** [Streamlit](https://streamlit.io/)  
- **Backend Processing:** Python  
- **OCR:** Tesseract / pdf2image / Pillow  
- **LLM Integration:** Google Gemini API  
- **Data Handling:** Pandas  

---



