import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import pandas as pd
import io
from langchain_core.prompts.prompt import PromptTemplate
from utils.extarct_db import extract_name_and_colums , read_excel_query , read_sql_query


load_dotenv()

key  = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=key)

model=genai.GenerativeModel('gemini-pro')



# Function to load gemini model

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text


    
# Defining the prompt 


prompt = PromptTemplate(
    input_variables= ["db","colums"],
    
    template=""" 
    You are an expert in converting English questions to SQL query!
    The SQL database has the name {db} and has the following columns - 
    {colums}\n\nFor example,\nExample 1 - How many entries of records are present?,
    the SQL command will be something like this SELECT COUNT(*) FROM {db} ;
    \nExample 2 - Tell me all the student​​s studying in Data Science class?,
    the SQL command will be something like this SELECT * FROM {db}
    where CLASS="Data Science";
    also the sql code should not have ``` in beginning or end and sql word in output 
    
    """
    
)  


st.header("ConversDB")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=None)


if uploaded_file is not None:

    
    file_type = uploaded_file.type
    allowed_file_extensions = ["application/octet-stream", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
    
    
    if file_type in allowed_file_extensions:
        
        print(uploaded_file.name)
        question=st.text_input("Input Prompt: " , key="input")
        submit = st.button("Query")     
        if file_type == "application/octet-stream":
            
            
            file_path = os.path.join(os.getcwd(), uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
                
            db_info = extract_name_and_colums(uploaded_file.name)
            
            p1 = prompt.format(db=db_info)
            
            

            if submit:
                
                
                response = get_gemini_response(question,p1)
                
                print(response)
                
                # response = read_sql_query(response, file_path)

                # # print(response)
                # formatted_response=model.generate_content(f"Format this {response} in the table format")
                # response_text = formatted_response.candidates[0].content.parts[0].text
                # # Splitting the response text into lines
                # lines = response_text.strip().split('\n')

                # # Extracting column names and data
                # columns = [col.strip() for col in lines[0].split('|') if col.strip()]
                # data = [dict(zip(columns, [item.strip() for item in line.split('|') if item.strip()])) for line in lines[2:]]

                # # Creating DataFrame
                # df = pd.DataFrame(data)
                # st.subheader("The Response is ")
                # st.table(df)
                # # for row in response:
                # #     print(row)
                # #     st.header(row)
                
                
                
        if file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                
                
                
            st.success("File type is allowed.")
            file_content = uploaded_file.read()
            df = pd.read_excel(uploaded_file)

            st.write("Excel Sheet Data:")
            st.write(df)

            conn = sqlite3.connect(":memory:")
            df.to_sql("excel_data", conn, index=False, if_exists="replace")

            query = st.text_area("Enter SQL query")
            
            if st.button("Run Query"):
                try:
   
                    result_df = pd.read_sql_query(query, conn)
                    st.write("Query Result:")
                    st.write(result_df)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            conn.close()
        
    else:
        st.error("File type is not allowed. Please upload a .db or .xlsx file.")
    
    
    


