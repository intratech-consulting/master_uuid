import mysql.connector
from mysql.connector import Error

def create_connection():
    """Maak een database connectie."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',  # IP adres van de Docker-host (of 'localhost' als je lokaal werkt)
            port=3306,  # De standaard MySQL-poort
            user='root',  # De MySQL-gebruikersnaam
            password='mypassword',  # Het wachtwoord voor de MySQL-gebruiker
            database='masterUuid'
        )
        print("Verbinding met MySQL DB succesvol")
    except Error as e:
        print(f"Fout bij het verbinden met MySQL: {e}")
    return connection

def insert_data(connection, data):
    """Voeg een nieuwe rij toe aan de database."""
    cursor = connection.cursor()
    query = """
    INSERT INTO masterUuid (fossbilling, salesforce, google_calendar, wordpress, odoo, sendgrid, inventree)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Data succesvol toegevoegd")
    except Error as e:
        print(f"Fout bij het toevoegen van data: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    conn = create_connection()
    if conn is not None:
        new_data = ('123', '456', '789', 'abc', 'def', 'ghi', 'jkl')
        insert_data(conn, new_data)
