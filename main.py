import json
from src.utils.openai_utils import extract_company_name, extract_po_details, extract_line_items
from src.utils.pdf_utils import extract_text_from_pdf
from src.utils.db_utils import insert_po_details
from app import display_items, app
import pandas as pd
import streamlit as st


def get_file_name():
    file_name = st.text_input("Enter the file name", value="keith-BEKPO125241-1.pdf")
    return file_name


def print_in_ui(line_items, po_number, po_dates, company_name):
    df_line_items = pd.DataFrame(line_items)
    df_line_items['PO Number'] = po_number
    df_line_items['PO Date'] = po_dates
    df_line_items['Company Name'] = company_name
    df_line_items['Line Item'] = df_line_items.index + 1
    df_line_items = df_line_items[['Company Name', 'PO Number', 'PO Date', 'Line Item'] + [col for col in df_line_items.columns if col not in ['Company Name', 'PO Number', 'PO Date', 'Line Item']]]
    # print(f'{df_line_items}')

    # Streamlit app to display the dataframe
    st.title("Purchase Order Details")
    st.write("Below are the extracted details from the PDF:")

    # Display the dataframe in Streamlit
    st.dataframe(df_line_items)



# Example Usage

# pdf_path = "pdf-samples/BEKPO854241.pdf"
# pdf_path = "pdf-samples/edi_po_2885865.pdf"
# pdf_path = "pdf-samples/305332_PO.pdf"
# pdf_path = "pdf-samples/PO#-219337.pdf"
# pdf_path = "Mcdonald_po_type1.pdf"
# pdf_path = "pdf-samples/Mcdonald_po_type2.pdf"
# pdf_path = "Mcdonald_po_type3.pdf"
# pdf_path = "Mcdonald_po_type4.pdf"
# pdf_path = "pdf-samples/Mcdonald_po_type5.pdf"
# pdf_path = "pdf-samples/DFIO_MLD30642.pdf"
# pdf_path = "pdf-samples/DFIO_JAN45319.pdf"
# pdf_path = "pdf-samples/FERCHA_PO_001526862_20250113.pdf"
# pdf_path = "pdf-samples/TJMAXX_DISTRIBUTION_INSTRUCTIONS_01_10_2025_0421_PM_343613_V1.pdf" # special case
# pdf_path = "pdf-samples/SG Purchase Order 4105003.pdf"
# pdf_path = "pdf-samples/PURORD-3.pdf"
# pdf_path = "pdf-samples/TORANI - EPICUREAN PO #A62460, #A62470, #A62480.pdf"
# pdf_path = "pdf-samples/sysco-LA-po-44802350.pdf"
# file_name = input("Enter the file name (default: pdf-data/keith-BEKPO125241-1.pdf): ") or "keith-BEKPO125241-1.pdf"
file_name = get_file_name()
pdf_path = f"pdf-data/{file_name}"
text = extract_text_from_pdf(pdf_path)
company_name = extract_company_name(text)
po_number, po_dates = extract_po_details(text, company_name)
line_items = extract_line_items(text, company_name)

# insert_po_details(company_name, po_number, po_dates, line_items)
print(f'PO number is {po_number}')
# print(line_items)
# Copy the line_items in to dataframe

print_in_ui(line_items, po_number, po_dates, company_name)


# items = display_items(po_number)
# print(json.dumps(items, indent=4))
# print(f"PO Numbers: {po_numbers}")
# print(f"PO Dates: {po_dates}")
# print(f"Line Items: {line_items}")


# '''
# 1. file name as argument
# 2. line items
# 3. insert in table
# '''
