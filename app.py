import streamlit as st
import plotly.express as px
from sql_agent import process_query
import pandas as pd

st.set_page_config(page_title="AI Data Analyst", page_icon="📊", layout="wide")

# ================================
# 🎨 PREMIUM CSS STYLING
# ================================
custom_css = """
<style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    #MainMenu, header, footer {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #111827; border-right: 1px solid #1f2937; }
    
    .title-text {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3.5rem;
        background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .subtitle-text { font-family: 'Inter', sans-serif; font-size: 1.2rem; color: #94a3b8; margin-bottom: 40px; }
    
    .stTextInput > div > div > input {
        border-radius: 12px; border: 2px solid #1f2937; background-color: #111827; color: white;
        padding: 15px; font-size: 1.1rem; transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus { border-color: #3b82f6; box-shadow: 0 0 15px rgba(59, 130, 246, 0.3); }
    
    .stButton > button {
        width: 100%; background: linear-gradient(90deg, #2563eb, #4f46e5); color: white;
        font-weight: bold; border-radius: 8px; border: none; padding: 12px; font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4); color: white; }
    
    .data-card {
        background-color: #111827; padding: 25px; border-radius: 15px; border: 1px solid #1f2937;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-top: 20px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ================================
# 🖥️ APPLICATION LAYOUT
# ================================
st.markdown('<p class="title-text">📊 Text-to-SQL BI Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Chat with your enterprise database. AI translates your English into an SQL Query, executes it, and visualizes the results.</p>', unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.shields.io/badge/Status-Connected-blue?style=for-the-badge", width=150)
    st.header("⚙️ Data Settings")
    st.info("""
    **Architecture:**
    * 🗣️ **NLP Engine:** LangChain
    * 🗄️ **Database:** SQLite
    * 🧠 **Brain:** Groq API
    * 📉 **Charts:** Plotly Express
    """)
    st.divider()
    groq_api_key = st.text_input("🔑 Groq API Key", type="password", placeholder="gsk_...")
    groq_model = st.selectbox("Select LLM Brain", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"], index=0)
    st.divider()
    st.markdown("**Database Schema Available:**")
    st.code("Table: Customers\n- customer_id\n- name\n- email\n- country\n- signup_date\n\nTable: Products\n- product_id\n- product_name\n- category\n- price\n\nTable: Sales\n- sale_id\n- customer_id\n- product_id\n- sale_date\n- quantity\n- total_amount")

# Main Input Section
col1, col2 = st.columns([4, 1])
with col1:
    question = st.text_input("💬 Ask your Data Analyst", placeholder="e.g. 'Show me the total quantity sold for each product category.'", label_visibility="collapsed")
with col2:
    start_button = st.button("🔍 Run Query")

# ================================
# ⚙️ EXECUTION LOOP
# ================================
if start_button:
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.status("🧠 **Translating English to SQL...**", expanded=True) as status_box:
            
            if not groq_api_key:
                st.error("Please provide your Groq API Key in the sidebar menu.")
                st.stop()
                
            result = process_query(question, groq_model, groq_api_key)
            
            # Show the generated SQL
            st.write("✅ **AI Generated SQL Query:**")
            st.code(result['sql'], language='sql')
            
            if result['error']:
                status_box.update(label="🚨 Query Failed", state="error", expanded=True)
                st.error(f"Execution Error: {result['error']}")
                st.info("Tip: Small local models sometimes write invalid SQL syntax. Try rephrasing your question or using a larger model.")
            else:
                df = result['df']
                status_box.update(label="📊 Data Retrieved Successfully!", state="complete", expanded=False)
                
                st.markdown('<div class="data-card">', unsafe_allow_html=True)
                
                # Check if data is empty
                if df is None or df.empty:
                    st.warning("The query executed successfully, but returned 0 rows (No data found).")
                else:
                    st.subheader("📋 Query Results")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # --- AUTO-CHARTING LOGIC ---
                    # If we have at least 1 text column and 1 numeric column, we can build a chart!
                    numeric_cols = df.select_dtypes(include='number').columns.tolist()
                    categorical_cols = df.select_dtypes(exclude='number').columns.tolist()
                    
                    if len(numeric_cols) >= 1 and len(categorical_cols) >= 1 and len(df) > 1:
                        st.divider()
                        st.subheader("📉 Auto-Generated Chart")
                        
                        # Plot first categorical vs first numeric
                        x_col = categorical_cols[0]
                        y_col = numeric_cols[0]
                        
                        try:
                            # If many rows, Bar Chart or Line Chart. If few, Pie Chart.
                            if len(df) <= 10:
                                fig = px.pie(df, names=x_col, values=y_col, hole=0.4, title=f"{y_col} by {x_col}")
                            else:
                                fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}", template="plotly_dark")
                            
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as chart_err:
                            st.warning(f"Could not instantly generate a chart for this specific data structure.")
                            
                st.markdown('</div>', unsafe_allow_html=True)
                st.balloons()
