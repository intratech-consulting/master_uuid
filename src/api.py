from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
    """ Make database connection """
    try:
        connection = mysql.connector.connect(
            host='mysql',
            port=3306,
            user='root',
            password='mypassword',
            database='masterUuid'
        )
        print("Connected successfully to the database.")
        return connection
    except Error as e:
        error_message = f"DB-connection Error: '{e}'"
        print(error_message)
        return error_message  # Return the error message

def insert_master_uuid(fossbilling, salesforce, google_calendar, wordpress, odoo, sendgrid, inventree):
    """ Add a new row to the masterUuid table """
    connection = create_connection()
    if isinstance(connection, str):  # Check if connection is an error message
        return jsonify({"error": connection}), 500  # Return error as JSON response
    
    cursor = connection.cursor()
    query = """
    INSERT INTO masterUuid (fossbilling, salesforce, google_calendar, wordpress, odoo, sendgrid, inventree)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    try:
        cursor.execute(query, (fossbilling, salesforce, google_calendar, wordpress, odoo, sendgrid, inventree))
        connection.commit()
        print("Data successfully added.")
        return jsonify({"success": True, "message": "Data successfully added."}), 201
    except Error as e:
        error_message = f"Failed to insert data: {e}"
        print(error_message)
        return jsonify({"error": error_message}), 500  # Return error as JSON response
    finally:
        cursor.close()
        connection.close()

@app.route('/add', methods=['POST'])
def add_entry():
    """ API endpoint for adding an entry """
    data = request.get_json()
    result = insert_master_uuid(**data)
    return result  # Return the response returned from insert_master_uuid

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
