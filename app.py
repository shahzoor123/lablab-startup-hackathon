import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import pandas as pd
import io
from langchain_core.prompts.prompt import PromptTemplate


load_dotenv()

key  = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=key)

model=genai.GenerativeModel('gemini-pro')



# Function to load gemini model

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text







def db_colums():
    try:
        # Connect to the database (replace 'student.db' with your database name)
        connection = sqlite3.connect('student.db')
        cursor = connection.cursor()

        # Execute a query to fetch all columns from a specific table (replace 'STUDENT' with your table name)
        cursor.execute("SELECT * FROM STUDENT")

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Print column names
        print("Column Names:", column_names)
        
        return column_names
    
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
    print(db)
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    connection.commit()
    connection.close()
    for row in rows:
        print(row)
    return rows

    
# Defining the prompt 


prompt=[
    """ 
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - 
    NAME, CLASS, SECTION \n\nFor example,\nExample 1 - How many entries of records are present?,
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the student​​s studying in Data Science class?,
    the SQL command will be something like this SELECT * FROM STUDENT
    where CLASS="Data Science";
    also the sql code should not have ``` in beginning or end and sql word in output 
    
    """
]





st.header("ConversDB")

 # Add a file uploader widget to the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a file", type=None)

# Add a file uploader widget to the sidebar

if uploaded_file is not None:

    
    file_type = uploaded_file.type

    # List of allowed file types
    allowed_file_extensions = ["application/octet-stream", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "text/csv"]
    
    if file_type in allowed_file_extensions:
        
        question=st.text_input("Input Prompt: " , key="input")
   
        submit = st.button("Query")     
        
        if file_type == "application/octet-stream":
            
            if submit:
                response = get_gemini_response(question,prompt)
                
                
                file_path = os.path.join(os.getcwd(), uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                response = read_sql_query(response, file_path)

                print(response)
                formatted_response=model.generate_content(f"Format this {response} in the table format")
                response_text = formatted_response.candidates[0].content.parts[0].text
                # Splitting the response text into lines
                lines = response_text.strip().split('\n')

                # Extracting column names and data
                columns = [col.strip() for col in lines[0].split('|') if col.strip()]
                data = [dict(zip(columns, [item.strip() for item in line.split('|') if item.strip()])) for line in lines[2:]]

                # Creating DataFrame
                df = pd.DataFrame(data)
                st.subheader("The Response is ")
                st.table(df)
                # for row in response:
                #     print(row)
                #     st.header(row)
                
                
                
        if file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                
                
                
            st.success("File type is allowed.")
            # Optionally, read and display the file content
            file_content = uploaded_file.read()
            
            df = pd.read_excel(uploaded_file)

            # Display the DataFrame
            st.write("Excel Sheet Data:")
            st.write(df)

            # Create an in-memory SQLite database
            conn = sqlite3.connect(":memory:")
            df.to_sql("excel_data", conn, index=False, if_exists="replace")

            # Get SQL query from the user
            query = st.text_area("Enter SQL query")
            
            

            if st.button("Run Query"):
                try:
                    # Execute the SQL query
                    result_df = pd.read_sql_query(query, conn)
                    st.write("Query Result:")
                    st.write(result_df)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            # Close the SQLite connection
            conn.close()
        
    else:
        st.error("File type is not allowed. Please upload a .db or .xlsx file.")
    
    
    


