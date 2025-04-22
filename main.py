import streamlit as st
import requests
import sqlite3

st.title("Text to SQL Generator")
user_input = st.text_input("Enter your natural language query:")

def get_data_from_database(sql_query):
    database = "student.db"
    with sqlite3.connect(database) as conn:
        return conn.execute(sql_query).fetchall()

if st.button("Generate SQL"):
    response = requests.post(
        "http://localhost:8000/generate-sql",
        json={"user_query": user_input}
    )

    if response.status_code == 200:
        result = response.json()
        sql_query = result['sql_query']

        st.success("SQL Query Generated:")
        st.code(sql_query, language="sql")

        try:
            retrieved_data = get_data_from_database(sql_query)
            st.header(f"🔍 Retrieving data from the database with the query:")
            if retrieved_data:
                for row in retrieved_data:
                    st.write(row)
            else:
                st.warning("No data found for this query.")
        except Exception as e:
            st.error(f"Database Error: {e}")

    else:
        st.error("Failed to get a response from backend.")


