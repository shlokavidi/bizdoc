import openai
import os
from dotenv import load_dotenv

from .db_utils import get_company_names, get_custom_text
from .json_utils import format_company_name, format_po_details, format_line_items

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_company_name(text):
    """
    Extracts the company name from the given text using OpenAI's ChatCompletion API.
    """
    company_names = get_company_names()
    prompt = (
        f'''Which company (customer) gave this PO to TORANI? Give in JSON format: 
        just the company name - "COMPANY_NAME". {text}. Map the company name to one of these names: {company_names}. 
        If the company name is not in the list, return "UNKNOWN".'''
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a data entry expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.5,
    )
    company_name = response.choices[0].message['content'].strip()
    return format_company_name(company_name)

def extract_po_details(pdf_text, company_name):
    """
    Extracts PO details (PO_Number and PO_Date) from the given text using OpenAI's ChatCompletion API.
    """
    generic_text = (
        '''Extract "PO_Number" and "PO_Date" from the given text. Give the output in json format: 
        {
            "PO_Number": po_number,
            "PO_Date": MM/DD/YYYY (in datetime format %m%d%Y, not string)
        }.'''
    )
    custom_text = get_custom_text(company_name)
    prompt = generic_text + custom_text if custom_text else generic_text
    final_prompt = f"We know that the company name is {company_name}. {prompt} TEXT STARTS HERE - {pdf_text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a data entry expert."},
            {"role": "user", "content": final_prompt}
        ],
        max_tokens=100,
        temperature=0.5,
    )
    po_details = response.choices[0].message['content'].strip()
    return format_po_details(po_details)

def extract_line_items(pdf_text, company_name):
    """
    Extracts line items from the given text using OpenAI's ChatCompletion API.
    """
    generic_text = (
        '''Extract line items from the given text. Expected json format: 
            {
                "Product_Number": "product_number", (also called product code, item code, item number, prod#, item#)
                "Product_Description": "product_description",
                "Quantity": "quantity", (NOT CALLED SIZE OR PACK it is always a number, either float or int)
                "Unit_Cost": "unit_cost" (ignore currency symbol, just the number)
            }
    Check for multiple line items. Ensure it is in json format.'''
    )
    custom_text = get_custom_text(company_name)
    prompt = generic_text + custom_text if custom_text else generic_text
    final_prompt = f"We know that the company name is {company_name}. {prompt}. TEXT STARTS HERE - {pdf_text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a data entry expert."},
            {"role": "user", "content": final_prompt}
        ],
        max_tokens=3000,
        temperature=0.5,
    )
    line_items = response.choices[0].message['content'].strip()
    line_items  = format_line_items(line_items)
    return line_items
