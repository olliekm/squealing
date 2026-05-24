from ollama import chat, Client, ChatResponse
from sqlalchemy import create_engine, text, inspect
from tabulate import tabulate
import re

engine = create_engine("sqlite:///CAvideos.db")

def get_schema(engine):
    inspector = inspect(engine)
    schema = []
    for table in inspector.get_table_names():
        cols = inspector.get_columns(table)
        col_defs = ", ".join(f"{c['name']} {c['type']}" for c in cols)
        schema.append(f"CREATE TABLE {table} ({col_defs})")
    return "\n".join(schema)

system_prompt = f"""You are a SQL expert. Given the following schema, write a SQLite query.

SCHEMA:
{get_schema(engine)}


Return only the SQL query, nothing else."""





client = Client()

def run_query(engine, sql):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        columns = list(result.keys())
        rows = result.fetchall()
        return columns, rows

def clean_response(raw):
    match = re.search(r"```(?:sql)?\n?(.*?)```", raw, re.DOTALL)
    return match.group(1).strip() if match else raw.strip()


def question(user_query = None):
    if user_query is None:
        while True:
            user_query = input("Ask about your data: ")
            if user_query == "quit":
                break
            response = client.chat(model='qwen2.5-coder:7b', messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ])
            
            cleaned_response = clean_response(response["message"]["content"])

            try:
                print(cleaned_response)

                # headers = clean_response.split("FROM")[0][5:].strip().split(",")
                # print(headers   )
                cols, query_result = run_query(engine, cleaned_response)
                table = tabulate(query_result, cols, tablefmt="grid")
                print(table)
            except:
                return "sorry this didnt work"




# print(response['message']['content'])

if __name__ == "__main__":
    while True:
        query = input("Input here: ")
        print(question(query))
