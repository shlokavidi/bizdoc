import json

def format_company_name(company_name):
    company_name = company_name.replace("```", "")
    company_name = company_name.replace('json', "")
    company_name = json.loads(company_name)
    name = company_name.get("COMPANY_NAME", "UNKNOWN")
    return name
