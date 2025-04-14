from db import connect_to_mysql

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