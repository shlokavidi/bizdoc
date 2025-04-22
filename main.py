import json
from src.utils.openai_utils import extract_company_name, extract_po_details, extract_line_items
from src.utils.pdf_utils import extract_text_from_pdf
from src.utils.db_utils import insert_po_details
from app import display_items, app
import pandas as pd
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import os


st.set_page_config(layout="wide")

def get_file_name():
    pdf_files = [f for f in os.listdir("demo-data")]
    file_name = st.selectbox("Select the file name", pdf_files, index=0)
    return file_name

def print_in_ui(file_name, line_items, po_number, po_dates, company_name):
    pdf_path = f"demo-data/{file_name}"
    col1, col2 = st.columns([1, 1])
    product_num = []
    product_description = []
    quantity = []
    unit_cost = []
    amount = []
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        with col1:
            pdf_viewer(pdf_data, width=800, height=1000)
    df_line_items = pd.DataFrame(line_items)
    with col2:
        st.write(f"**Company Name:** {company_name}")
        st.write(f"**PO Number:** {po_number}")
        st.write(f"**PO Date:** {po_dates}")
        for item in line_items:
            product_num.append(item[0])
            product_description.append(item[1])
            quantity.append(item[2])
            unit_cost.append(item[3])   
            amount.append(item[2] * item[3])
        df_line_items['Product Number'] = product_num
        df_line_items['Product Description'] = product_description
        df_line_items['Quantity'] = quantity
        df_line_items['Unit Cost'] = unit_cost
        df_line_items['Amount'] = amount
        df_line_items = df_line_items[[ 'Product Number', 'Product Description', 'Quantity', 'Unit Cost', 'Amount']]
        st.dataframe(df_line_items)


file_name = get_file_name()
pdf_path = f"demo-data/{file_name}"
text = extract_text_from_pdf(pdf_path)
print(text)
company_name = extract_company_name(text)
po_number, po_dates = extract_po_details(text, company_name)
line_items = extract_line_items(text, company_name)
print(line_items)

print_in_ui(file_name, line_items, po_number, po_dates, company_name)
