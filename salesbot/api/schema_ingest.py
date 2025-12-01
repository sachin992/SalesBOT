import pymysql
from dotenv import load_dotenv
import os


load_dotenv()


def build_schema_text():
    conn = pymysql.connect(host='127.0.0.1', user=os.getenv('DB_USER','Sachin'), password=os.getenv('DB_PASS','Sadpli@123'), db='sales_db')
    out = []
    with conn.cursor() as cur:
        cur.execute("SHOW TABLES")
        tables = [t[0] for t in cur.fetchall()]
        for t in tables:
            cur.execute(f"SHOW COLUMNS FROM `{t}`")
            cols = cur.fetchall()
            col_text = ', '.join([f"{c[0]} ({c[1]})" for c in cols])
            out.append(f"TABLE {t}: {col_text}")
    conn.close()


    schema_text = '\n'.join(out)
    # Save to file for Django to load
    with open('cached_schema.txt', 'w') as f:
        f.write(schema_text)
        print('Wrote cached_schema.txt')


if __name__ == '__main__':
    build_schema_text()