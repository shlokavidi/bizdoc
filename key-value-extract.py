import pdfplumber
import openai

def extract_text_from_pdf(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

def extract_key_value_pairs(text):
    text = 'PO#987654 2025-04-05 ShipTo:MCD Prim,456ElmSt,Springfield,IL62701 Item#12345 TORANI SYRUP VANILLA Qty:20 Price:22.15'
    company_names = ['MCDONALD PRIMARY', 'KEHE FOOD DISTRIBUTORS INC', 'BEN E. KEITH CO.', 'MCDONALD SECONDARY', 'BIRITE FOODSERVICE DISTRIBUTORS']
    openai.api_key = 'token'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            # {"role": "user", "content": f''''Extract PO Number, PO Date, Ship To Name, Ship To Adress, Ship To City, Ship To State, Ship to Zip, Item Number, Item Description, Item Quantity, Item Price in json format. sample outputs are given in annotations.json file.
            # \n\n{text}'''}
            {"role": "user", "content": f'''Which company (customer) gave this PO to TORANI? Give in json format just the company name - "COMPANY_NAME"{text}. Map the company name to one of these names: {company_names}'''}
        ],
        max_tokens=500,
        temperature=0.5,
    )
    return response.choices[0].message['content'].strip()

# Example Usage

# pdf_path = "BEKPO854241.pdf"
# pdf_path = "edi_po_2885865.pdf"
# pdf_path = "305332_PO.pdf"
# pdf_path = "PO#-219337.pdf"
pdf_path = "Mcdonald_po_type1.pdf"
pdf_path = "Mcdonald_po_type2.pdf"
pdf_path = "Mcdonald_po_type3.pdf"
pdf_path = "Mcdonald_po_type4.pdf"
pdf_path = "Mcdonald_po_type5.pdf"
text = extract_text_from_pdf(pdf_path)
key_value_pairs = extract_key_value_pairs(text)
print(key_value_pairs)
# print(text)
