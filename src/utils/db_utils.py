from db import connect_to_mysql
from datetime import datetime

def get_company_names():
    """
    Fetch company names from the database and return them as a list.
    """
    connection = connect_to_mysql()
    if connection is None:
        return []

    with connection.cursor() as cursor:
        cursor.execute("SELECT company_name FROM company")
        rows = cursor.fetchall()

    connection.close()
    return [row[0] for row in rows]

def get_custom_text(company_name):
    """
    Fetch custom text for a given company name from the database.
    """
    connection = connect_to_mysql()
    if connection is None:
        return None

    with connection.cursor() as cursor:
        cursor.execute("SELECT po_customization FROM company WHERE company_name = %s", (company_name,))
        row = cursor.fetchone()

        cursor.fetchall() 

    connection.close()
    return row[0] if row else None


def insert_po_details(company_name, po_number, po_date, line_items):
    """
    Insert PO details into the database.
    """
    connection = connect_to_mysql()
    if connection is None:
        return
    for item in line_items:
        product_num = item[0]
        product_description = item[1]
        quantity = item[2]
        unit_cost = item[3]
        amount = quantity * unit_cost
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO order_details (company_name, po_number, po_date, product_num, prod_description, quantity, unit_cost, amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (company_name, po_number, po_date, product_num, product_description, quantity, unit_cost, amount)
            )
            connection.commit()
    
    print(f"Inserted PO details for {company_name} into the database.")

    connection.close()