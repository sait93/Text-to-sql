import sqlite3

# create database 
connection=sqlite3.connect("student.db")

#create cursor
cursor=connection.cursor()

create_table_query = """
create table if not exists student(
    NAME varchar(25),
    COURSE varchar(25),
    SECTION varchar(25),
    MARKS int
);
"""

cursor.execute(create_table_query)
# ID INTEGER PRIMARY KEY AUTOINCREMENT,
# cursor.execute("DELETE FROM student")

#insert records 
sql_query = """Insert into student(NAME, COURSE, SECTION, MARKS) VALUES (?,?,?,?) """
values=[
    ('student1','data Science','A',90),
    ('student2','data Science','b',100),
    ('student3','data Science','A',86),
    ('student4','devops','A',50),
    ('student5','devops','A',35),
    ('student6','crm developer','c',90)
]

cursor.executemany(sql_query,values)
connection.commit()

data=cursor.execute("""select * from student""")

for row in data:
    print(row)

if connection:
    connection.close()

