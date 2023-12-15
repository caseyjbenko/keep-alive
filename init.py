import sqlite3
import os

DATABASE_PATH = 'endpoints.db'  # Update with the desired path for your SQLite database

def create_table(db_file):
    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # SQL to create the table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS devices (
        ip_address TEXT PRIMARY KEY,
        mac_address TEXT NOT NULL,
        tag TEXT
    );
    """

    # Execute the create table command
    cur.execute(create_table_sql)
    conn.commit()
    conn.close()

def main():
    # Check if the database file already exists
    if not os.path.exists(DATABASE_PATH):
        print("Creating new database...")
        create_table(DATABASE_PATH)
        print("Database and table created successfully.")
    else:
        print("Database already exists. No action was taken.")

if __name__ == "__main__":
    main()

