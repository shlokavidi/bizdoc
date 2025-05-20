import os
import openai
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import pdfplumber

def convert_pdf_to_image(pdf_path):
    """
    Convert a PDF file to an image using pdf2image.
    """
    images = convert_from_path(pdf_path)
    image_name = os.path.basename(pdf_path).replace('.pdf', '')
    output_dir = os.path.join("demo-data", image_name)
    os.makedirs(output_dir, exist_ok=True)
    output_paths = []
    for i, image in enumerate(images):
        output_path = os.path.join(output_dir, f"output_image_page_{i + 1}.jpg")
        image.save(output_path, "JPEG")
        output_paths.append(output_path)
    return output_paths  # Return the list of paths to the saved images
    images[0].save(output_path, "JPEG")  # Save the first page as an image
    return output_path  # Return the path to the saved image

def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.
    """
    # Use Tesseract OCR to extract text from the image
    extracted_text = pytesseract.image_to_string(Image.open(image_path))
    return extracted_text



def extract_text_from_pdf(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text