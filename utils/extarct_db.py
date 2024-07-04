import sqlite3

def extract_name_and_colums(db):
    try:
        # Connect to the database (replace 'student.db' with your database name)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        
        all_tables_and_columns = {}
        
        for_table = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = for_table.fetchall()
        
        for table in tables:
            table_name = table[0]
            cur.execute(f"PRAGMA table_info({table_name});")
            columns = cur.fetchall()
            column_names = [col[1] for col in columns]
            all_tables_and_columns[table_name] = column_names
        

        # Extract table names from the query result
        table_name = [table[0] for table in tables]
        
   
        return  {"table_name": table_name , "colum_names" : all_tables_and_columns}
    
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the connection
        if connection:
            connection.close()
            
            
            
def read_excel_query():
    pass



# Function to retrive query from the
def read_sql_query(sql,db):
    
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    connection.commit()
    connection.close()
    # for row in rows:
    #     # print(row)
    return rows