import json

def format_company_name(company_name):
    company_name = company_name.replace("```", "")
    company_name = company_name.replace('json', "")
    company_name = json.loads(company_name)
    name = company_name.get("COMPANY_NAME", "UNKNOWN")
    return name

def format_po_details(po_details):
    po_details = po_details.replace("```", "")
    po_details = po_details.replace('json', "")
    po_details = json.loads(po_details)
    po_number = po_details.get("PO_Number")
    po_date = po_details.get("PO_Date")
    return po_number, po_date
