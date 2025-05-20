# '''
# 1. Convert PDF to image
# 2. Extract text from the image using OCR
# 3. Process the extracted text with OpenAI API
# '''

# import os
# from dotenv import load_dotenv
# import openai
# from PIL import Image
# from pdf2image import convert_from_path
# import pytesseract

# # Load environment variables from .env file
# load_dotenv()

# # Set OpenAI API key from environment variable
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def convert_pdf_to_image(pdf_path):
#     """
#     Convert a PDF file to an image using pdf2image.
#     """
#     images = convert_from_path(pdf_path)
#     output_path = "output_image.jpg"
#     images[0].save(output_path, "JPEG")  # Save the first page as an image
#     return output_path  # Return the path to the saved image

# def extract_text_from_image(image_path):
#     """
#     Extract text from an image using Tesseract OCR.
#     """
#     # Use Tesseract OCR to extract text from the image
#     extracted_text = pytesseract.image_to_string(Image.open(image_path))
#     return extracted_text

# def process_text_with_openai(extracted_text):
#     """
#     Process the extracted text with OpenAI's API.
#     """
#     prompt = f"Extract PO Number and other details from the following text:\n{extracted_text}"
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a data entry expert."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=1000,
#         temperature=0.1,
#     )
#     return response.choices[0].message['content'].strip()

# # Example usage
# pdf_path = "C:/Users/vidis/Documents/bizdoc/demo-data/BEK1.pdf"
# # pdf_path = "C:/Users/vidis/Documents/bizdoc/demo-data/PFS-Alabama.PDF"
# image_path = convert_pdf_to_image(pdf_path)
# # print(f"Image saved at: {image_path}")

# extracted_text = extract_text_from_image(image_path)
# print(extracted_text)

# # processed_data = process_text_with_openai(extracted_text)
# # print(f"Processed Data: {processed_data}")