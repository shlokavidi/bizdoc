import openai
import os
from dotenv import load_dotenv

from .db_utils import get_company_names, get_custom_text
from .json_utils import format_company_name

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_company_name(text):
    # text = 'PO#987654 2025-04-05 ShipTo:MCD Prim,456ElmSt,Springfield,IL62701 Item#12345 TORANI SYRUP VANILLA Qty:20 Price:22.15'
    company_names = get_company_names()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f'''Which company (customer) gave this PO to TORANI? Give in json format 
             just the company name - "COMPANY_NAME"{text}. Map the company name to one of these names: {company_names}. 
             "Performance Foodservice" is "5 ETHAN SURRETT".
             If the company name is not in the list, return "UNKNOWN". 
             '''}
        ],
        max_tokens=500,
        temperature=0.5,
    )
    company_name = response.choices[0].message['content'].strip()
    return format_company_name(company_name)
    
    

def extract_po_details(pdf_text, company_name):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    generic_text = '''Extract "PO_Number" and "PO_Date" (format MM/DD/YYYY) from the given text. Expected format - 
    {
        "PO_Number": ["po_number"],
        "PO_Date": ["MM/DD/YYYY"]
    }.
    Check for multiple PO numbers and dates.'''
    custom_text = get_custom_text(company_name)
    # print(f"Custom Text: {custom_text}")
    prompt = generic_text + custom_text if custom_text else generic_text
    final_prompt = f'''We know that the company name is {company_name}. {prompt}TEXT STARTS HERE - {pdf_text}'''
    # print(f"Final Prompt: {final_prompt}")
    # print(f"Prompt: {prompt}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f'''{final_prompt}'''}
        ],
        max_tokens=500,
        temperature=0.5,
    )
    return response.choices[0].message['content'].strip()