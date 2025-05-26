import google.generativeai as genai
import os
import json
from tabulate import tabulate
from dotenv import load_dotenv
# from .db_utils import get_company_names
from .db_utils import get_company_names
from .json_utils import format_line_items

load_dotenv()

# Configure evnironment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
        company_names = get_company_names()
        # Upload the PDF file to be processed by Gemini.
        # Ensure 'pdf_path' variable (function argument) points to your PDF file.
        # Add error handling for genai.upload_file if needed in a production scenario.
        uploaded_pdf_file = genai.upload_file(path=pdf_path, display_name="Purchase Order Document")

        # Define the textual part of your prompt.
        # Instruct the model to extract information from the provided PDF.
        instruction_prompt_text = """
            You are an expert at extracting information from purchase orders.
            From the provided PDF document, please extract the Customer Name , PO number, PO date, and the Pickup/Ship to address.
            Return this information as a JSON object.
            If any piece of information cannot be found, use null as its value.
            Format the output as follows:
            {
            "customer_name": "Customer Name",
            "po_number": "PO12345",
            "po_date": "10/26/2023",
            "pickup": "123 Main St, Anytown, CA 90210"
            }
            Match the customer name to one of these names: {company_names}.
            Date should be in MM/DD/YYYY format.
        """

        # The 'prompt' will now be a list containing the instructions (text)
        # and the uploaded file object. This is how you provide multimodal input.
        prompt = [
            instruction_prompt_text,
            uploaded_pdf_file
        ]

        response = model.generate_content(prompt)

        if response and response.text:
            try:

                # Clean the response text to remove potential markdown formatting
                cleaned_text = response.text.strip()
                if cleaned_text.startswith("```json"):
                    cleaned_text = cleaned_text[7:]
                if cleaned_text.endswith("```"):
                    cleaned_text = cleaned_text[:-3]
                
                extracted_data = json.loads(cleaned_text)
                print(f"extracted_data: {extracted_data}")
                if extracted_data:
                    table = [[k, v] for k, v in extracted_data.items()]
                    print(tabulate(table, headers=["Field", "Value"], tablefmt="grid"))
                else:
                    print("No data extracted to display in table.")

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


def extract_line_items_gemini(pdf_path):
    """
    Extracts line items from a PDF using Gemini AI.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: A list of dictionaries containing line item details, or None on failure.
    """
    try:
        # Upload the PDF file to be processed by Gemini.
        uploaded_pdf_file = genai.upload_file(path=pdf_path, display_name="Purchase Order Document")

        # Define the textual part of your prompt.
        instruction_prompt_text = """
            You are an expert at extracting line items from purchase orders.
            From the provided PDF document, please extract the line items including Product Number, Product Description, Quantity, and Unit Cost.
            Return this information as a JSON array of objects.
            If any piece of information cannot be found, use null as its value.
            Format the output as follows:
            {
                "Product_Number": "product_number", (also called product code, item code, item number, prod#, item#)
                "Product_Description": "product_description",
                "Quantity": "quantity", (NOT CALLED SIZE OR PACK it is always a number, either float or int)
                "Unit_Cost": "unit_cost" (ignore currency symbol, just the number)
            }
        """

        # The 'prompt' will now be a list containing the instructions (text)
        # and the uploaded file object. This is how you provide multimodal input.
        prompt = [
            instruction_prompt_text,
            uploaded_pdf_file
        ]

        response = model.generate_content(prompt)

        if response and response.text:
            try:
                cleaned_text = response.text.strip()
                if cleaned_text.startswith("```json"):
                    cleaned_text = cleaned_text[7:]
                if cleaned_text.endswith("```"):
                    cleaned_text = cleaned_text[:-3]
                
                # line_items = json.loads(cleaned_text)
                line_items = format_line_items(cleaned_text)  # Format the line items if needed
                return line_items
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            print("Gemini API returned an empty or invalid response.")
            return None

    except Exception as e:
        print(f"Error extracting line items: {e}")
        return None
    
    
res = extract_line_items_gemini('C:/Users/vidis/Documents/bizdoc/demo-data/BEK1.pdf')
print(res)