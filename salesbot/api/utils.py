import os
import openai
import sqlparse
from django.db import connection
from dotenv import load_dotenv


load_dotenv()

from openai import OpenAI



# Prompt template
PROMPT_TEMPLATE = '''You are an expert SQL generator for a MySQL sales database.
- Only produce valid, syntactically correct SELECT statements.
- Do NOT produce INSERT/UPDATE/DELETE/DROP statements.
- Assume the following schema (always use exact column/table names):


{schema}


User question: "{nl_query}"


Return ONLY the SQL statement. Do not add any explanation.'''





def generate_sql(schema_text, nl_query):
    system_prompt = f"""
    You are an expert SQL generator. Generate only SQL for MySQL based on the schema below.
    Schema:
    {schema_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",   # change model if needed
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": nl_query}
        ],
        temperature=0.1
    )

    sql_text = response.choices[0].message.content.strip()
    print("Generated SQL:", sql_text)
    return sql_text







# Validation: only SELECT


def is_select_only(sql_text: str) -> bool:
    parsed = sqlparse.parse(sql_text)
    if not parsed:
        return False
    
    
    # Very basic check: first token contains 'SELECT'
    first = sql_text.strip().lower()
    return first.startswith('select')


# Execute safely (read-only user)


def execute_sql(sql_text: str):
    with connection.cursor() as cursor:
        cursor.execute(sql_text)
        columns = [col[0] for col in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        # convert to list of dicts
        data = [dict(zip(columns, row)) for row in rows]
    return {'columns': columns, 'rows': data}