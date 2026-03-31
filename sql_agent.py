from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain.chains import create_sql_query_chain
import pandas as pd
import sqlite3
import re

def process_query(question: str, model_name: str, api_key: str) -> dict:
    """Translates a natural language question into SQL, runs it, and returns the data."""
    
    db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
    llm = ChatGroq(model_name=model_name, api_key=api_key, temperature=0.0)
    
    # Create the SQL generating chain
    chain = create_sql_query_chain(llm, db)
    
    sql_query = ""
    try:
        # Step 1: Tell the LLM to write the SQL query
        raw_output = chain.invoke({"question": question + " Return ONLY the valid SQL code, no markdown formatting, no explanations, and do not use ? or other parameterized placeholders."})
        
        # Step 2: Clean the output (Small LLMs often wrap code in backticks despite instructions)
        sql_query = raw_output.replace("```sql", "").replace("```", "").strip()
        
        # Strip conversational text often appended by small models predicting the rest of the prompt
        sql_query = re.split(r'^\s*(?:SQLResult:|Answer:|Explanation:)', sql_query, flags=re.IGNORECASE | re.MULTILINE)[0]

        # Extract everything from SELECT/WITH onwards (removes conversational prefixes)
        match = re.search(r'\b(SELECT|WITH|INSERT|UPDATE|DELETE)\b.*', sql_query, flags=re.IGNORECASE | re.DOTALL)
        if match:
            sql_query = match.group(0)
            
        # Security: Remove any potential destructive trailing commands
        sql_query = sql_query.split(";")[0].strip(' \n\r\t"\'') + ";" 
        
        # Step 3: Execute the SQL via Pandas
        conn = sqlite3.connect('ecommerce.db')
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        
        return {"sql": sql_query, "df": df, "error": None}
        
    except Exception as e:
        err_msg = str(e)
        return {"sql": sql_query, "df": None, "error": err_msg}
