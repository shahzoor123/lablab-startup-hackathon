import google.generativeai as genai
from dotenv import load_dotenv
from langchain_core.prompts.prompt import PromptTemplate
import os
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain.chains import LLMChain , SimpleSequentialChain , SequentialChain
from openai.types.chat.chat_completion import ChatCompletion

load_dotenv()



API = os.getenv("OPEN_API_KEY")


model = OpenAI(api_key=API)


prompt = PromptTemplate(
    input_variables= ["db","colum"],
    
    template = " You are an expert in converting English questions to SQL query! The SQL database has the name {db} and has the following columns - {colum}\n\nFor example,\nExample 1 - How many entries of records are present?,the SQL command will be something like this SELECT COUNT(*) FROM {db} ;\nExample 2 - Tell me all the student​​s studying in Data Science class?,the SQL command will be something like this SELECT * FROM {db} where CLASS= Data Science; also the sql code should not have ``` in beginning or end and sql word in output "

) 


db = "STUDENT"
colum = ["NAME", "CLASS", "SECTION"]
            

p1 = prompt.format(db=db, colum=colum)



response = model.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system","content": [{"type": "text","text": p1}]},
    {"role": "user", "content": "show all students list"}
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response.choices[0].message.content)










 








