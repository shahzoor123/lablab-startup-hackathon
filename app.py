import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import pandas as pd
import io
<<<<<<< HEAD
from langchain_core.prompts.prompt import PromptTemplate
=======
from langchain.prompts import PromptTemplate
>>>>>>> c7bcaa51ac1a7d6ed7b93a9ef5072b5448fc1544
from utils.extarct_db import extract_name_and_colums , read_excel_query , read_sql_query
from typing import List
import numpy as np

import matplotlib.pyplot as plt


load_dotenv()

key  = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=key)

model=genai.GenerativeModel('gemini-pro')



# Function to load gemini model


def get_gemini_response(question: str, table_name: str, column_names: List[str]) -> str:
    # Convert column_names list to a comma-separated string
    columns_str = ', '.join(column_names)
    
    # Defining the prompt
    prompt = PromptTemplate(
        input_variables=["table_name", "columns"],
        template=""" 
        You are an expert in converting English questions to SQL query!
        The SQL database has the name {table_name} and has the following columns - 
        {columns}\n\nFor example,\nExample 1 - How many entries of records are present?,
        the SQL command will be something like this SELECT COUNT(*) FROM {table_name} ;
        \nExample 2 - Tell me all the students studying in Data Science class?,
        the SQL command will be something like this SELECT * FROM {table_name}
        where CLASS="Data Science";
        and remove "_" underscore between colum names show like Full Name
        also the sql code should not have ``` in beginning or end and sql word in output 
        
        """
    )
    
    # Format the prompt with the table_name and columns_str
    formatted_prompt = prompt.format(table_name=table_name, columns=columns_str)
    
    # Assuming genai is correctly imported and configured
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([formatted_prompt, question])
    return response.text
    
st.header("ConverseDB")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=None)


if uploaded_file is not None:

    
    file_type = uploaded_file.type
    allowed_file_extensions = ["application/octet-stream"]
    
    
    if file_type in allowed_file_extensions:
        
        print(uploaded_file.name)
        question=st.text_input("Input Prompt: " , key="input")
        submit = st.button("Query")     
        if file_type == "application/octet-stream":
            
            
            file_path = os.path.join(os.getcwd(), uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
                            
            db_info = extract_name_and_colums(uploaded_file.name)
            table_name = db_info['table_name'][0]
            column_names = db_info['colum_names']['STUDENT']
            
            print(column_names)

            if submit:
                response = get_gemini_response(question, table_name, column_names)
                print(response)
                            
                response = read_sql_query(response, file_path)

                # print(response)
                formatted_response=model.generate_content(f"Format this {response} in the table format")
                response_text = formatted_response.candidates[0].content.parts[0].text
                # Splitting the response text into lines
                lines = response_text.strip().split('\n')
                
                print(lines)

                # Extracting column names and data
                columns = [col.strip() for col in lines[0].split('|') if col.strip()]
                data = [dict(zip(columns, [item.strip() for item in line.split('|') if item.strip()])) for line in lines[2:]]

                print(columns,data)
                # Creating DataFrame
                df = pd.DataFrame(data)
                st.subheader("The Response is ")
                st.table(df)
                # for row in response:
                #     print(row)
                # #     st.header(row)
                

                
                # # Convert to DataFrame
                # df = pd.DataFrame(data, columns=columns)

             
            
                # chart_data = pd.DataFrame(df, columns=column_names)

                # st.bar_chart(chart_data)
                
                 
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        # if file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            
        #     # converting excel file to db format then deleting excel file
        #     db_name = "data.db"
        #     file_path = os.path.join(os.getcwd(), uploaded_file.name)
        #     with open(file_path, "wb") as f:
        #         f.write(uploaded_file.getbuffer())

        #     df = pd.read_excel(file_path)
        #     conn = sqlite3.connect(db_name)
        #     df.to_sql("excel_data", conn, index=False, if_exists="replace")
        #     conn.close()
        #     # os.remove(file_path)
            
            
        #     # extracting DB Name & colum names
            
        #     db_info = extract_name_and_colums(db_name)
        #     table_name = db_info['table_name'][0]
        #     column_names = db_info['colum_names']
            
        #     print(column_names)
            
            
        #     if submit:
        #         response = get_gemini_response(question, table_name, column_names)
        #         print(response)
                            
        #         response = read_sql_query(response, db_name)

        #         # print(response)
        #         formatted_response=model.generate_content(f"Format this {response} in the table format")
        #         response_text = formatted_response.candidates[0].content.parts[0].text
        #         # Splitting the response text into lines
        #         lines = response_text.strip().split('\n')

        #         # Extracting column names and data
        #         columns = [col.strip() for col in lines[0].split('|') if col.strip()]
        #         data = [dict(zip(columns, [item.strip() for item in line.split('|') if item.strip()])) for line in lines[2:]]

        #         # Creating DataFrame
        #         df = pd.DataFrame(data)
        #         st.subheader("The Response is ")
        #         st.table(df)
        #         # for row in response:
        #         #     print(row)
        #         # #     st.header(row)
            

        # else:
        #     st.error("File type is not allowed. Please upload a .db or .xlsx file.")
    
    
    


