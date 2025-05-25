import pdfplumber
import re
import google.generativeai as genai
import os
import json
from tabulate import tabulate

APP_HOME_DIR = '/Users/gridharanvidi/coding_work/bizdoc/demo-data'
# PDF_FILENAME = 'BiRite.pdf'
PDF_FILENAME = 'Mcdonald_po_type1.pdf'

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("No GEMINI_API_KEY found in environment variables. Please set the GEMINI_API_KEY environment variable.")
genai.configure(api_key=GEMINI_API_KEY)  # Replace with your actual Gemini API key
# model = genai.GenerativeModel('gemini-1.5-pro-latest')
model = genai.GenerativeModel('gemini-2.0-flash')

def extract_po_data_gemini(pdf_path):
    """
    Extracts PO data using Gemini AI.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        dict: A dictionary containing the extracted data, or None on failure.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        # Note: The text extraction using pdfplumber (the 'with pdfplumber.open...' block
        # and the loop that populates the 'text' variable) immediately preceding this
        # section is no longer necessary if you are sending the PDF directly to Gemini.
        # You may want to remove that text extraction code.

        # Upload the PDF file to be processed by Gemini.
        # Ensure 'pdf_path' variable (function argument) points to your PDF file.
        # Add error handling for genai.upload_file if needed in a production scenario.
        uploaded_pdf_file = genai.upload_file(path=pdf_path, display_name="Purchase Order Document")

        # Define the textual part of your prompt.
        # Instruct the model to extract information from the provided PDF.
        instruction_prompt_text = """
            You are an expert at extracting information from purchase orders.
            From the provided PDF document, please extract the PO number, PO date, and the Pickup address.
            Return this information as a JSON object.
            If any piece of information cannot be found, use null as its value.
            For example:
            {
            "po_number": "PO12345",
            "po_date": "2023-10-26",
            "pickup": "123 Main St, Anytown, CA 90210"
            "email" : "name@abc.com"
            }

            Similarly read all the header key value pair and return in JSON format.
            """

        # The 'prompt' will now be a list containing the instructions (text)
        # and the uploaded file object. This is how you provide multimodal input.
        prompt = [
            instruction_prompt_text,
            uploaded_pdf_file
        ]

        response = model.generate_content(prompt)
        print(f"reponse: {response}")
        # Basic error handling for the response (Improve as needed)
        if response and response.text:
            try:

                # Clean the response text to remove potential markdown formatting
                cleaned_text = response.text.strip()
                if cleaned_text.startswith("```json"):
                    cleaned_text = cleaned_text[7:]
                if cleaned_text.endswith("```"):
                    cleaned_text = cleaned_text[:-3]
                
                extracted_data = json.loads(cleaned_text)
                return extracted_data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            print("Gemini API returned an empty or invalid response.")
            return None

    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

if __name__ == '__main__':
    pdf_file = f"{APP_HOME_DIR}/{PDF_FILENAME}"  # Replace with your PDF file path
    extracted_data = extract_po_data_gemini(pdf_file)

    if extracted_data:
        print("Extracted Data:")
        print(f"PO Number: {extracted_data.get('po_number')}")
        print(f"PO Date: {extracted_data.get('po_date')}")
        print(f"Pickup address: {extracted_data.get('pickup')}")
        print(f"Email: {extracted_data.get('email')}")
    else:
        print("Could not extract data from the PDF.")

    # Prepare data for tabular display
    if extracted_data:
        table = [[k, v] for k, v in extracted_data.items()]
        print(tabulate(table, headers=["Field", "Value"], tablefmt="grid"))
    else:
        print("No data extracted to display in table.")
