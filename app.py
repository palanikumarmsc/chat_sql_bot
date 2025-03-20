import os
import re
import sqlite3
import datetime
import random
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from langchain_community.llms.huggingface_hub import HuggingFaceHub

# Load environment variables
load_dotenv()

# Hugging Face Model Setup
model_id = os.getenv("MODEL_NAME")
huggingface_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

llm = HuggingFaceHub(
    repo_id=model_id,
    huggingfacehub_api_token=huggingface_api_key,
    model_kwargs={"temperature": 0.1, "max_new_tokens": 1024, "top_k": 50, "repetition_penalty": 1.03},
)

# Function to initialize SQLite database
def initialize_db():
    conn = sqlite3.connect("sales_data.db")
    cursor = conn.cursor()

    # Create Sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT,
            Product TEXT,
            Quantity INTEGER,
            Price REAL
        )
    """)
    conn.commit()
    conn.close()

# Function to generate and insert sample sales data (Runs only once)
def populate_sales_data():
    conn = sqlite3.connect("sales_data.db")
    cursor = conn.cursor()

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM Sales")
    if cursor.fetchone()[0] == 0:
        start_date = datetime.date(2025, 1, 1)  # Jan 1, 2025
        num_days = 100

        products = ["Product A", "Product B", "Product C", "Product D"]
        data = []

        for i in range(num_days):
            date = start_date + datetime.timedelta(days=i)  # Generate sequential dates
            product = random.choice(products)  # Randomly select a product
            quantity = random.randint(1, 20)  # Random quantity between 1 and 20
            price = random.choice([100, 150, 200, 250, 300])  # Random price

            data.append((date.strftime('%Y-%m-%d'), product, quantity, price))

        cursor.executemany("INSERT INTO Sales (Date, Product, Quantity, Price) VALUES (?, ?, ?, ?)", data)
        conn.commit()

    conn.close()

# ✅ Initialize database and populate sample data
initialize_db()
populate_sales_data()

# Function to generate an SQLite query using Hugging Face API
import datetime

def generate_sql_query(user_query):
    schema_info = """
    Table: Sales
    Columns:
      - Date (TEXT): Date of sale (YYYY-MM-DD)
      - Product (TEXT): Name of the product sold
      - Quantity (INTEGER): Number of units sold
      - Price (REAL): Price per unit
    """

    # Get current month & year dynamically
    current_year_month = datetime.datetime.now().strftime('%Y-%m')

    prompt = f"""
    You are an AI SQL Generator designed to create **SQLite-compatible SQL queries**.

    - Use **valid SQLite SQL syntax**.
    - Apply **WHERE** conditions **only if required**.
    - If the user asks for a specific **month or year**, format it correctly:
      - Use `strftime('%Y-%m', DATE(Date)) = '{current_year_month}'` for filtering by the current month.
      - Use `strftime('%Y', DATE(Date)) = 'YYYY'` if filtering by year.
      - Use `Date = 'YYYY-MM-DD'` if filtering by a specific day.
    - If no date filter is mentioned, do not include a WHERE clause.
    - Use `SUM(Quantity)`, `COUNT(*)`, `AVG(Price)`, or `DISTINCT` as needed.
    - Ensure column names match exactly with the schema.
    - **Return only the SQL query**, no explanations or additional text.

    Table Schema:
    {schema_info}

    User Query: {user_query}

    SQL Query:
    """
    
    response = llm.invoke(prompt).strip()

    # Ensure the response is not empty
    if not response or "SELECT" not in response.upper():
        return "SELECT 'Error: No valid SQL query generated';"

    return response



def extract_sql_query(text):
    # First, try to extract the query enclosed in triple backticks
    pattern_triple_backticks = r"```(?:sql)?\s*(SELECT .*?)\s*```"
    match = re.search(pattern_triple_backticks, text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()  # Return the SQL query inside triple backticks
    
    # If no match, try to find a query that starts with SELECT and ends with ;
    pattern_select = r"SELECT\s.*?;"
    match = re.search(pattern_select, text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(0).strip()  # Return the matched query
    
    return "No valid SQL query found."

# Function to execute SQL query on SQLite
def execute_sql_query(sql_query):
    try:
        conn = sqlite3.connect("sales_data.db")
        result_df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return result_df
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("📊 Chat with SQL Bot (SQLite)")
st.write("Ask questions about the sales data.")

# User input
user_query = st.text_area("Enter your query:")

if st.button("Submit"):
    if user_query:
        st.write("Generating SQL Query...")

        # Generate SQL query
        sql_query = generate_sql_query(user_query)
        # st.write(f"**Generated SQL Query:** `{sql_query}`")

        # Extract SQL Query
        sql_query = extract_sql_query(sql_query)

        # sql_query = "SELECT Date FROM Sales;"
        
        # Execute the SQL query
        st.write(sql_query)


        result = execute_sql_query(sql_query)

        if isinstance(result, pd.DataFrame):
            st.write("### Query Result:")
            st.write(result)
        else:
            st.error(f"Error executing query: {result}")
