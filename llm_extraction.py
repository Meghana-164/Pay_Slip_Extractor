# utils/llm_extraction.py
import google.generativeai as genai
from config import GEMINI_API_KEY
import json

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_fields_from_text(text):
    prompt = f"""
You are an intelligent assistant. From the KYC document text below, extract the following fields and respond ONLY in JSON format:
{{
  "Name": string or null,
  "Father's Name": string or null,
  "Occupation": string or null,
  "Amount": string or null,
  "Address": string or null,
  "Company Name": string or null,
  "PAN ID": string or null,
  "Aadhar ID": string or null
}}

If any field is not available, return null for that field.

KYC Document Text:
{text}
"""
    try:
        response = model.generate_content(prompt)
        json_start = response.text.find("{")
        json_end = response.text.rfind("}") + 1
        json_string = response.text[json_start:json_end]
        data = json.loads(json_string)
        return data
    except Exception as e:
        return {
            "error": f"❌ Gemini returned invalid JSON: {str(e)}\n\nRaw response:\n{response.text if 'response' in locals() else 'undefined'}"
        }
