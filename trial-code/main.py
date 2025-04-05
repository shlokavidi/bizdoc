import pdfplumber

def extract_text_from_pdf(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

# Example Usage
pdf_path = "BEKPO854241.pdf"
text = extract_text_from_pdf(pdf_path)
print(text)

