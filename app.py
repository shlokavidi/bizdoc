from flask import Flask, jsonify, request
import mysql.connector
from src.utils.openai_utils import extract_company_name, extract_po_details, extract_line_items
from src.utils.pdf_utils import extract_text_from_pdf
from src.utils.db_utils import insert_po_details
from db import connect_to_mysql

app = Flask(__name__)

# Function to process a PDF and extract details
# @app.route('/api/process_pdf', methods=['POST'])
# def process_pdf():
#     data = request.json
#     file_name = data.get("file_name")
#     if not file_name:
#         return jsonify({"error": "File name is required"}), 400

#     pdf_path = f"pdf-samples/{file_name}"
#     try:
#         text = extract_text_from_pdf(pdf_path)
#         company_name = extract_company_name(text)
#         po_number, po_date = extract_po_details(text, company_name)  # <-- line 22
#         line_items = extract_line_items(text, company_name)

#         # Insert details into the database
#         insert_po_details(company_name, po_number, po_date, line_items)

#         # Return the PO number (and anything else you need)
#         return jsonify({
#             "po_number": po_number,
#             "po_date": str(po_date),
#             "company_name": company_name,
#             "line_items": line_items
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
# Function to fetch items from the database
def get_items_from_db(po_number):
    connection = connect_to_mysql()
    if connection is None:
        return None

    with connection.cursor(dictionary=True) as cursor:
        query = "SELECT * FROM order_details WHERE po_number = %s;"
        cursor.execute(query, (po_number,))
        rows = cursor.fetchall()

    connection.close()
    return rows if rows else None

# API route to fetch items by PO number
@app.route('/api/items', methods=['GET'])
def display_items(po_number):
    print("Fetching items for PO number:", po_number)
    if not po_number:
        return jsonify({"error": "PO number is required"}), 400

    items = get_items_from_db(po_number)
    if not items:
        return jsonify({"message": "No items found for the given PO number"}), 404

    return(jsonify(items))

if __name__ == '__main__':
    app.run(debug=True)