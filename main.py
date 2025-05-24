import json
from src.utils.openai_utils import extract_company_name, extract_po_details, extract_line_items
from src.utils.pdf_utils import extract_text_from_image, convert_pdf_to_image, extract_text_from_pdf
from src.utils.db_utils import insert_po_details
import pandas as pd
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import os
import base64


st.set_page_config(layout="wide")

def get_file_name():
    pdf_files = [f for f in os.listdir("demo-data")]
    file_name = st.selectbox("Select the file name", pdf_files, index=0)
    return file_name


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)



def print_in_ui(file_name, line_items, po_number, po_dates, company_name):
    pdf_path = f"demo-data/{file_name}"
    col1, col2 = st.columns(2)

    with col1:
        st.write("### PDF Preview")
        show_pdf(pdf_path)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name=file_name,
                mime="application/pdf"
            )

    with col2:
        st.write(f"**Company Name:** {company_name}")
        st.write(f"**PO Number:** {po_number}")
        st.write(f"**PO Date:** {po_dates}")

        # Prepare DataFrame
        df_line_items = pd.DataFrame(line_items, columns=['Product Number', 'Product Description', 'Quantity', 'Unit Cost'])
        if not df_line_items.empty:
            df_line_items['Amount'] = df_line_items['Quantity'] * df_line_items['Unit Cost']
            st.dataframe(df_line_items)
            st.write("**Total Quantity:**", df_line_items['Quantity'].sum())
            st.write("**Total Amount:**", df_line_items['Amount'].sum())
        else:
            st.write("No line items found.")


file_name = get_file_name()
pdf_path = f"demo-data/{file_name}"
# pdf_path = "demo-data/ImperialDade.PDF"
text = extract_text_from_pdf(pdf_path)
company_name = extract_company_name(text)
po_number, po_dates = extract_po_details(text, company_name)
line_items = extract_line_items(text, company_name)
insert_po_details(company_name, po_number, po_dates, line_items)

print_in_ui(file_name, line_items, po_number, po_dates, company_name)
