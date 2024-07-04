import sqlite3 


connection= sqlite3.connect("student.db")

cursor = connection.cursor()

table_info = """
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25));
"""


cursor.execute(table_info)


# Inserting Some more records


cursor.execute('''Insert Into STUDENT values('Faraz', 'Computer Science', 'A')''')
cursor.execute('''Insert Into STUDENT values('Alice', 'Mathematics', 'B')''')
cursor.execute('''Insert Into STUDENT values('Bob', 'Physics', 'C')''')
cursor.execute('''Insert Into STUDENT values('Charlie', 'Chemistry', 'A')''')
cursor.execute('''Insert Into STUDENT values('David', 'Biology', 'B')''')
cursor.execute('''Insert Into STUDENT values('Ella', 'Computer Science', 'A')''')
cursor.execute('''Insert Into STUDENT values('Frank', 'Mathematics', 'C')''')
cursor.execute('''Insert Into STUDENT values('Grace', 'Physics', 'B')''')
cursor.execute('''Insert Into STUDENT values('Hannah', 'Chemistry', 'A')''')
cursor.execute('''Insert Into STUDENT values('Ivy', 'Biology', 'C')''')
cursor.execute('''Insert Into STUDENT values('Jack', 'Computer Science', 'A')''')
cursor.execute('''Insert Into STUDENT values('Kate', 'Mathematics', 'B')''')
cursor.execute('''Insert Into STUDENT values('Liam', 'Physics', 'A')''')
cursor.execute('''Insert Into STUDENT values('Mia', 'Chemistry', 'C')''')
cursor.execute('''Insert Into STUDENT values('Noah', 'Biology', 'B')''')
cursor.execute('''Insert Into STUDENT values('Olivia', 'Computer Science', 'A')''')
cursor.execute('''Insert Into STUDENT values('Peter', 'Mathematics', 'C')''')
cursor.execute('''Insert Into STUDENT values('Quinn', 'Physics', 'B')''')
cursor.execute('''Insert Into STUDENT values('Rose', 'Chemistry', 'A')''')
cursor.execute('''Insert Into STUDENT values('Sam', 'Biology', 'C')''')



# Display all the records

print("The inserted records are")
data = cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)
    
connection.commit()
connection.close()