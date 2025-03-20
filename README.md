# 📊 Chat with SQL Bot (SQLite) - Python Streamlit Application

## 📌 Overview
This Python application enables users to interact with a **SQL bot** through a **Streamlit UI**. The bot answers queries related to sales data stored in an SQLite database, utilizing `LangChain` and the `HuggingFace API` for natural language processing.

## 🚀 Features
- **Sample Sales Data Generation**: Automatically populates an SQLite database (`sales_data.db`) with sample sales data.
- **User Query Handling**: Accepts natural language queries about the sales data.
- **AI-Powered SQL Generation**: Uses the `Mistral-7B` model from Hugging Face to translate user queries into SQL statements.
- **Query Execution**: Executes the generated SQL queries on the SQLite database.
- **Results Display**: Presents query results within the Streamlit interface.

## 📂 Project Structure
```
chat_excel_bot/
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
├── app.py                # Main Python application
├── sales_data.db         # SQLite database with sample sales data
```

## 🛠️ Prerequisites
- **Python 3.x** installed ([Download Python](https://www.python.org/downloads/))
- **Visual Studio Code** ([Download VS Code](https://code.visualstudio.com/))

## ✅ Step 1: Install VS Code Extensions
1. Open VS Code.
2. Navigate to **Extensions (`Ctrl + Shift + X`)**.
3. Install the following extensions:
   - **Python** (Microsoft)
   - **Pylance**
   - **Jupyter** (if using notebooks)
   - **autopep8** (for code formatting)

## ✅ Step 2: Clone the Repository & Set Up Project
```bash
git clone https://github.com/palanikumarmsc/chat_excel_bot.git
cd chat_excel_bot
```

## ✅ Step 3: Set Up a Virtual Environment
```bash
python -m venv venv
```
Activate the virtual environment:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

## ✅ Step 4: Install Dependencies
Ensure your `requirements.txt` includes:
```
streamlit
pandas
python-dotenv
langchain
huggingface_hub
```
Then install the dependencies:
```bash
pip install -r requirements.txt
```

## ✅ Step 5: Configure the `.env` File
Create a `.env` file and add:
```
MODEL_NAME='mistralai/Mistral-7B-Instruct-v0.3'
HUGGINGFACEHUB_API_TOKEN='your_huggingface_api_key'
```
Replace `'your_huggingface_api_key'` with your actual **Hugging Face API token**.

## ✅ Step 6: Run the Application
```bash
streamlit run app.py
```
Access the application in your browser at:
```
http://localhost:8501
```

## ✅ Step 7: Debugging in VS Code
1. Navigate to **Run** → **Add Configuration** → Select **Python**.
2. Add the following configuration in `.vscode/launch.json`:
   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Python: Streamlit",
               "type": "python",
               "request": "launch",
               "program": "${workspaceFolder}/app.py",
               "console": "integratedTerminal"
           }
       ]
   }
   ```
3. Press **F5** or click **Run and Debug** to start debugging.

## 🎯 Example Usage
- **User Query:**
  ```
  How many Product A sales were made this month?
  ```
- **Generated SQL Query:**
  ```sql
  SELECT SUM(Quantity) FROM Sales WHERE Product = 'Product A' AND strftime('%Y-%m', Date) = '2025-03';
  ```
- **Result Displayed in Streamlit UI** 🎉

## 📝 Sample Queries to Test the AI SQL Generator Bot
1. **List all sales records.**
   ```sql
   SELECT * FROM Sales;
   ```
2. **Show the total quantity of products sold in March 2025.**
   ```sql
   SELECT SUM(Quantity) FROM Sales WHERE strftime('%Y-%m', Date) = '2025-03';
   ```
3. **Retrieve all sales for the product 'Laptop' in February 2024.**
   ```sql
   SELECT * FROM Sales WHERE Product = 'Laptop' AND strftime('%Y-%m', Date) = '2024-02';
   ```
4. **Get the average price of products sold in 2023.**
   ```sql
   SELECT AVG(Price) FROM Sales WHERE strftime('%Y', Date) = '2023';
   ```
5. **Find the total revenue (Quantity * Price) for each product in the current month.**
   ```sql
   SELECT Product, SUM(Quantity * Price) AS TotalRevenue FROM Sales WHERE strftime('%Y-%m', Date) = '2025-03' GROUP BY Product;
   ```
6. **List distinct products sold in the last 7 days.**
   ```sql
   SELECT DISTINCT Product FROM Sales WHERE Date >= date('now', '-7 days');
   ```
7. **Show all sales transactions made on '2025-03-15'.**
   ```sql
   SELECT * FROM Sales WHERE Date = '2025-03-15';
   ```
8. **Retrieve the total number of sales transactions in the year 2024.**
   ```sql
   SELECT COUNT(*) FROM Sales WHERE strftime('%Y', Date) = '2024';
   ```
9. **List all sales where more than 10 units were sold in a single transaction.**
   ```sql
   SELECT * FROM Sales WHERE Quantity > 10;
   ```
10. **Find the top 5 best-selling products based on quantity sold.**
    ```sql
    SELECT Product, SUM(Quantity) AS TotalSold FROM Sales GROUP BY Product ORDER BY TotalSold DESC LIMIT 5;
    ```

## ✅ Next Steps
- **Enhance Query Parsing**: Improve the bot's ability to understand and process complex queries.
- **User Query Analytics**: Implement functionality to store and analyze user queries and responses.
- **Custom Data Upload**: Allow users to upload and interact with their own sales data.

