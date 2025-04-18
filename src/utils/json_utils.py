import json
from datetime import datetime

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
    po_date = datetime.strptime(po_date, "%m/%d/%Y").date()
    return po_number, po_date

def format_line_items(line_items):
    line_items = line_items.replace("```", "")
    line_items = line_items.replace('json', "")
    line_items = json.loads(line_items)
    
    formatted_items = []
    
    for item in line_items:
        product_num = item.get("Product_Number")
        product_description = item.get("Product_Description")
        quantity = item.get("Quantity")
        quantity = round(float(quantity), 2)
        unit_cost = item.get("Unit_Cost")
        unit_cost = round(float(unit_cost), 2)
        formatted_items.append([product_num, product_description, quantity, unit_cost])
    return formatted_items
