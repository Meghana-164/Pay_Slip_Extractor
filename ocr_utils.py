# utils/ocr_utils.py
import easyocr
from PIL import Image
from pdf2image import convert_from_path
import numpy as np
import tempfile

reader = easyocr.Reader(['en'])

def extract_text_from_image(image):
    # Ensure image is in NumPy format
    if isinstance(image, Image.Image):
        image = np.array(image)
    results = reader.readtext(image, detail=0)
    return '\n'.join(results)

def extract_text_from_pdf(file):
    text = ""
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name
    # Convert PDF to images
    images = convert_from_path(tmp_path)
    for img in images:
        text += extract_text_from_image(img) + "\n"
    return text

def process_document(file):
    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    else:
        image = Image.open(file)
        return extract_text_from_image(image)
