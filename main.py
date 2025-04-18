import streamlit as st 
import os
import  sqlite3

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate



def get_sql_query_from_text(user_query):
    groq_sys_prompt= ChatPromptTemplate.from_template("""
            you are an expert in converting english questions to SQL query!
            The SQL database has the name STUDENT and has the following columns - NAME, COURSE,SECTION and marks.
            For example, Example 1 - How many entries of records are present?, the sql command will be something like this SELECT count(*) from student;
            example 2 - Tell me all the studnts studying in the data science course?, the sql command will be something like this Select * from student where course="data science";
            also the sql code should not have ''' in beginning or end and sql word in output.
            now convert the following question in the engilsh to a vaild Sql Query:{user_query}.
            No preamble, only vaild Sql please""") 
    model="llama3-8b-8192"
    llm=ChatGroq(
        groq_api_key= os.environ.get("Groq_api_key"),
        model_name=model)

    chain = groq_sys_prompt | llm | StrOutputParser()
    sql_query = chain.invoke({"user_query":user_query})

    return sql_query

def get_data_from_database(sql_query):
    database="student.db"
    with sqlite3.connect(database) as conn:
        return conn.execute(sql_query).fetchall()


def main():
    st.set_page_config(page_title="Text To SQL")
    st.header("Talk to your database")

    user_query=st.text_input("Input:")
    submit=st.button("Enter") 
    if submit:
        sql_query =get_sql_query_from_text(user_query)
        retrieved_data=get_data_from_database(sql_query)
        st.header(f"Retrieving data from the database with the query:[{sql_query}]")
        for row in retrieved_data:
            st.header(row)

if __name__ == '__main__':
    main()
    