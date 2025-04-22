from fastapi import FastAPI
from pydantic import BaseModel
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    user_query: str

@app.post("/generate-sql")
def generate_sql(req: QueryRequest):
    prompt = ChatPromptTemplate.from_template("""
        You are an expert in converting English questions to SQL queries.
        The database has a table named STUDENT with columns: NAME, COURSE, SECTION, MARKS.
        Convert this question into a valid SQL query (no preamble or explanation): {user_query}
    """)

    llm = ChatGroq(
        groq_api_key=os.environ.get("Groq_api_key"),
        model_name="llama3-8b-8192"
    )

    chain = prompt | llm | StrOutputParser()
    sql = chain.invoke({"user_query": req.user_query})

    return {"sql_query": sql}
