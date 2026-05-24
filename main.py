from ollama import chat, Client, ChatResponse
from sqlalchemy import create_engine, text
import re

engine = create_engine("sqlite:///mydb.db")

system_prompt = f"""You are a SQL expert. Given the following schema, write a SQLite query.

SCHEMA:

Return only the SQL query, nothing else."""


client = Client()

def run_query(engine, sql):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return result.fetchall()

def clean_response(raw):
    match = re.search(r"```(?:sql)?\n?(.*?)```", raw, re.DOTALL)
    return match.group(1).strip() if match else raw.strip()


def question(user_query):
    response = client.chat(model='qwen2.5-coder:7b', messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query},
    ])
    
    cleaned_response = clean_response(response["message"]["content"])

    try:
        return run_query(cleaned_response)
    except:
        return "sorry this didnt work"


    


# print(response['message']['content'])

if __name__ == "__main__":
    query = input("Input here: ")
    print(question(query))
