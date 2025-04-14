from db import connect_to_mysql

def get_company_names():
    """
    Fetch company names from the database and return them as a list.
    """
    connection = connect_to_mysql()
    if connection is None:
        return []

    cursor = connection.cursor()
    cursor.execute("SELECT company_name FROM company")
    rows = cursor.fetchall()

    # Extract company names from the rows
    company_names = [row[0] for row in rows]

    cursor.close()
    connection.close()

    return company_names

def get_custom_text(company_name):
    """
    Fetch custom text for a given company name from the database.
    """
    connection = connect_to_mysql()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("SELECT po_customization FROM company WHERE company_name = %s", (company_name,))
    row = cursor.fetchone()

    cursor.fetchall()
    
    cursor.close()
    connection.close()

    if row:
        return row[0]
    else:
        return None
    
    
# text = get_custom_text("5 ETHAN SURRETT")
# print(text)
