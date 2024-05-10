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


def insert_master_uuid(id, fossbilling=None, salesforce=None, google_calendar=None, wordpress=None, odoo=None, sendgrid=None, inventree=None):
    """ Add a new row to the masterUuid table """
    connection = create_connection()
    if isinstance(connection, str):  # connection error, returning as an error message
        return False, {"error": connection}, 500

    cursor = connection.cursor()
    query = """
    INSERT INTO masterUuid (id, fossbilling, salesforce, google_calendar, wordpress, odoo, sendgrid, inventree)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    try:
        cursor.execute(query, (id, fossbilling, salesforce, google_calendar, wordpress, odoo, sendgrid, inventree))
        connection.commit()
        print("Data successfully added.")
        return True, {"success": True, "MasterUuid": id, "message": "Data successfully added."}, 201
    except Error as e:
        error_message = f"Failed to insert data: {e}"
        print(error_message)
        return False, {"error": error_message}, 500
    finally:
        cursor.close()
        connection.close()


@app.route('/createMasterUuid', methods=['POST'])
def create_master_uuid():
    """ API endpoint for creating a master UUID """
    data = request.get_json()
    service_id = data.get("ServiceId")
    service_name = data.get("Service")

    new_uuid = str(uuid.uuid4())
    id_dict = {service_name: service_id}

    success, response_body, status_code = insert_master_uuid(id=new_uuid, **id_dict)

    if not success:
        return jsonify(response_body), status_code
    else:
        return jsonify(response_body), status_code


@app.route('/addServiceId', methods=['POST'])
def add_service_id():
    """ API endpoint for adding a service ID to an existing master UUID """

    data = request.get_json()
    master_uuid = data.get("MasterUuid")
    service_id = data.get("ServiceId")
    service_name = data.get("ServiceName")

    # Connect to the database and attempt to update the record
    connection = create_connection()
    if isinstance(connection, str):  # Check if connection is an error message
        return jsonify({"error": connection}), 500  # Return error as JSON response

    cursor = connection.cursor()
    query = f"""
    UPDATE masterUuid
    SET {service_name} = %s
    WHERE id = %s;
    """
    try:
        cursor.execute(query, (service_id, master_uuid))
        if cursor.rowcount == 0:  # No record was updated
            return jsonify({"error": "No such UUID found."}), 404
        connection.commit()  # Commit the transaction if update was successful
        return jsonify({"success": True, "message": "Service ID successfully added."}), 200
    except Error as e:
        error_message = f"Failed to update data: {e}"
        print(error_message)
        return jsonify({"error": error_message}), 500  # Return error as JSON response
    finally:
        cursor.close()
        connection.close()

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
    master_uuid = data.get('MASTERUUID')
    new_service_id = data.get('NewServiceId')
    service_name = data.get('Service')

    connection = create_connection()
    if isinstance(connection, str):  # Check if connection is an error message
        return jsonify({"error": connection}), 500  # Return error as JSON response

    cursor = connection.cursor()
    query = """
    UPDATE masterUuid SET {} = %s WHERE id = %s;
    """.format(service_name)
    try:
        cursor.execute(query, (new_service_id, master_uuid))
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
    app.run(host='0.0.0.0', port=6000, debug=True)
