import sqlite3

def extract_name_and_colums(db):
    try:
        # Connect to the database (replace 'student.db' with your database name)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()

        # Extract table names from the query result
        table_names = [table[0] for table in tables]
        
        

        print(table_names)
    
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the connection
        if connection:
            connection.close()
            
db_name = 'db/student.db'
table_names = extract_name_and_colums(db_name)
