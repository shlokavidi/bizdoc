from src.utils.openai_utils import extract_company_name, extract_po_details
from src.utils.pdf_utils import extract_text_from_pdf

# Example Usage

# pdf_path = "pdf-samples/BEKPO854241.pdf"
# pdf_path = "pdf-samples/edi_po_2885865.pdf"
# pdf_path = "pdf-samples/305332_PO.pdf"
# pdf_path = "pdf-samples/PO#-219337.pdf"
# pdf_path = "Mcdonald_po_type1.pdf"
# pdf_path = "Mcdonald_po_type2.pdf"
# pdf_path = "Mcdonald_po_type3.pdf"
# pdf_path = "Mcdonald_po_type4.pdf"
pdf_path = "pdf-samples/Mcdonald_po_type5.pdf"
# pdf_path = "pdf-samples/DFIO_MLD30642.pdf"
# pdf_path = "pdf-samples/DFIO_JAN45319.pdf"
# pdf_path = "pdf-samples/FERCHA_PO_001526862_20250113.pdf"
# pdf_path = "pdf-samples/TJMAXX_DISTRIBUTION_INSTRUCTIONS_01_10_2025_0421_PM_343613_V1.pdf"
# pdf_path = "pdf-samples/SG Purchase Order 4105003.pdf"
# pdf_path = "pdf-samples/PURORD-3.pdf"
pdf_path = "pdf-samples/TORANI - EPICUREAN PO #A62460, #A62470, #A62480.pdf"
# pdf_path = "pdf-samples/sysco-LA-po-44802350.pdf"
text = extract_text_from_pdf(pdf_path)
company_name = extract_company_name(text)

print(f"Company Name: {company_name}")
po_details = extract_po_details(text, company_name)

print(f"PO Details: {po_details}")

   
