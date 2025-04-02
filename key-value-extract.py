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
    openai.api_key = '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'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f''''Extract PO Number, PO Date, Ship To Name, Ship To Adress, Ship To City, Ship To State, Ship to Zip, Item Number, Item Description, Item Quantity, Item Price in json format. sample outputs are given in annotations.json file.
            \n\n{text}'''}
        ],
        max_tokens=500,
        temperature=0.5,
    )
    return response.choices[0].message['content'].strip()

# Example Usage
pdf_path = "BEKPO854241.pdf"
# pdf_path = "edi_po_2885865.pdf"
# pdf_path = "305332_PO.pdf"
text = extract_text_from_pdf(pdf_path)
key_value_pairs = extract_key_value_pairs(text)
print(key_value_pairs)
# print(text)
