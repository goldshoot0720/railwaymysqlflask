from flask import Flask, jsonify
import os
from dotenv import load_dotenv
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
load_dotenv()

# 取得 MySQL 連線設定
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT")),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

ALLOWED_TABLES = {
    "article", "bank", "cloud", "experience", "food", "host",
    "inventory", "mail", "member", "routine", "subscription", "video"
}

def select_table(table_name):
    if table_name not in ALLOWED_TABLES:
        raise Exception(f"Table '{table_name}' not allowed.")
    
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM `{table_name}`")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    # 將資料轉換為 dict 列表
    result = [dict(zip(columns, row)) for row in rows]
    return result

@app.route("/")
def index():
    return """
<ul>
<li><a href="/article">article</a></li>
<li><a href="/bank">bank</a></li>
<li><a href="/cloud">cloud</a></li>
<li><a href="/experience">experience</a></li>
<li><a href="/food">food</a></li>
<li><a href="/host">host</a></li>
<li><a href="/inventory">inventory</a></li>
<li><a href="/mail">mail</a></li>
<li><a href="/member">member</a></li>
<li><a href="/routine">routine</a></li>
<li><a href="/subscription">subscription</a></li>
<li><a href="/video">video</a></li>
</ul>
"""

@app.route("/<table_name>")
def get_table(table_name):
    try:
        rows = select_table(table_name)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
