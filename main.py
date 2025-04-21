import json
from src.utils.openai_utils import extract_company_name, extract_po_details, extract_line_items
from src.utils.pdf_utils import extract_text_from_pdf
from src.utils.db_utils import insert_po_details
from app import display_items, app
import pandas as pd
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import os


def get_file_name():
    pdf_files = [f for f in os.listdir("pdf-data") if f.endswith(".pdf")]
    file_name = st.selectbox("Select the file name", pdf_files, index=0)
    
    # Display the selected PDF file
    pdf_path = f"pdf-data/{file_name}"
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        pdf_viewer(pdf_data, width=700, height=800)

    return file_name

def print_in_ui(line_items, po_number, po_dates, company_name):
    df_line_items = pd.DataFrame(line_items)
    df_line_items['PO Number'] = po_number
    df_line_items['PO Date'] = po_dates
    df_line_items['Company Name'] = company_name
    for item in line_items:
        product_num = item[0]
        product_description = item[1]
        quantity = item[2]
        unit_cost = item[3]    
        amount = quantity * unit_cost
    df_line_items['Product Number'] = product_num
    df_line_items['Product Description'] = product_description
    df_line_items['Quantity'] = quantity
    df_line_items['Unit Cost'] = unit_cost
    df_line_items['Amount'] = amount
    df_line_items = df_line_items[['Company Name', 'PO Number', 'PO Date', 'Product Number', 'Product Description', 'Quantity', 'Unit Cost', 'Amount']]

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
