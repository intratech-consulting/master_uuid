import uuid
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from migrations import create_master_uuid_table

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
    INSERT INTO masterUuid (id, fossbilling, salesforce, google_calendar, wordpress, odoo, sendgrid, inventree)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    # Generate a UUID
    id = str(uuid.uuid4())
    try:
        cursor.execute(query, (id, fossbilling, salesforce, google_calendar, wordpress, odoo, sendgrid, inventree))
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


@app.route('/getMasterUuid', methods=['POST'])
def get_master_uuid():
    """ API endpoint for getting a master UUID """
    data = request.get_json()
    service_id = data.get('ServiceId')
    service_name = data.get('Service')

    connection = create_connection()
    if isinstance(connection, str):  # Check if connection is an error message
        return jsonify({"error": connection}), 500  # Return error as JSON response

    cursor = connection.cursor()
    query = """
    SELECT id FROM masterUuid WHERE {} = %s;
    """.format(service_name)
    try:
        cursor.execute(query, (service_id,))
        result = cursor.fetchone()
        if result:
            return jsonify({"MASTERUUID": result[0]}), 200
        else:
            return jsonify({"error": "No matching entry found."}), 404
    except Error as e:
        error_message = f"Failed to fetch data: {e}"
        print(error_message)
        return jsonify({"error": error_message}), 500  # Return error as JSON response
    finally:
        cursor.close()
        connection.close()

@app.route('/UpdateServiceId', methods=['POST'])
def update_service_id():
    """ API endpoint for updating a service ID """
    data = request.get_json()
    service_id = data.get('ServiceId')
    service_name = data.get('Service')

    connection = create_connection()
    if isinstance(connection, str):  # Check if connection is an error message
        return jsonify({"error": connection}), 500  # Return error as JSON response

    cursor = connection.cursor()
    query = """
    UPDATE masterUuid SET {} = %s WHERE id = (SELECT id FROM masterUuid WHERE {} = %s);
    """.format(service_name, service_name)
    try:
        cursor.execute(query, (service_id, service_id))
        connection.commit()
        if cursor.rowcount:
            return jsonify({"success": True, "message": "Data successfully updated."}), 200
        else:
            return jsonify({"error": "No matching entry found."}), 404
    except Error as e:
        error_message = f"Failed to update data: {e}"
        print(error_message)
        return jsonify({"error": error_message}), 500  # Return error as JSON response
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    create_master_uuid_table()
    app.run(host='0.0.0.0', port=6000, debug=True)
