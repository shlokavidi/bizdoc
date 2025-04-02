'''
This program reads a PO (Purhcase Order) file extracts the data from and uploads into a MySQL database.
'''

import os
import sys
import csv
import PyPDF2

import mysql.connector

def connect_to_db():
    '''
    Connect to the MySQL database.
    '''
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='gridharan',
            database='po_db'
        )

        return conn
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)
        
def create_table():
    '''
    Create a table in the MySQL database.
    '''
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE po (
            po_number INT PRIMARY KEY,
            po_date DATE,
            vendor_name VARCHAR(255),
            vendor_address VARCHAR(255),
            vendor_city VARCHAR(255),
            vendor_state VARCHAR(255),
            vendor_zip VARCHAR(255),
            item_number INT,
            item_description VARCHAR(255),
            item_quantity INT,
            item_price FLOAT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(po_data):
    '''
    Insert the data into the MySQL database.
    '''
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO po (
            po_number, po_date, vendor_name, vendor_address, vendor_city, vendor_state, vendor_zip,
            item_number, item_description, item_quantity, item_price
        )
        VALUES ('
        ''')
    conn.commit()
    conn.close()

def parse_po_file(po_file):
    '''
    Parse the PO PDF file and extract the data from it.
    '''
    with open(po_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()

    # Assuming the PDF text is structured in a way that can be split into rows
    lines = text.split('\n')
    po_data = []
    for line in lines:
        # Process each line to extract relevant data
        # This part will depend on the structure of the PDF content
        row = line.split(',')  # Example: splitting by commas
        po_data.append(row)

    for row in po_data:
        print(row)
        # insert_data(row)

def main():
    '''
    Main function.
    '''
    if len(sys.argv) != 2:
        print('Usage: python parse_po.py <po_file>')
        sys.exit(1)
    po_file = sys.argv[1]
    if not os.path.exists(po_file):
        print(f'Error: {po_file} not found')
        sys.exit(1)
    parse_po_file(po_file)

if __name__ == '__main__':
    main()

    