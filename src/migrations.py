import mysql.connector
from mysql.connector import Error

def create_connection():
    """ Make database connection """
    try:
        # Connect to MySQL server without specifying a database
        connection = mysql.connector.connect(
            host='mysql_masteruuid',
            port=3306,
            user='root',
            password='mypassword'
        )
        cursor = connection.cursor()

        # Check if the 'masterUuid' database exists and create it if it doesn't
        cursor.execute("CREATE DATABASE IF NOT EXISTS masterUuid")
        connection.commit()

        # Close the connection and cursor
        cursor.close()
        connection.close()

        # Connect to the 'masterUuid' database
        connection = mysql.connector.connect(
            host='mysql_masteruuid',
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



def create_master_uuid_table():
    """ Create masterUuid table if it doesn't exist """
    connection = create_connection()
    if isinstance(connection, str):  # Check if connection is an error message
        return {"error": connection}  # Return error as JSON response

    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS masterUuid (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fossbilling VARCHAR(255),
        salesforce VARCHAR(255),
        google_calendar VARCHAR(255),
        wordpress VARCHAR(255),
        odoo VARCHAR(255),
        sendgrid VARCHAR(255),
        inventree VARCHAR(255)
    );
    """
    try:
        cursor.execute(query)
        connection.commit()
        print("Table successfully created.")
        return {"success": True, "message": "Table successfully created."}
    except Error as e:
        error_message = f"Failed to create table: {e}"
        print(error_message)
        return {"error": error_message}  # Return error as JSON response
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    create_master_uuid_table()