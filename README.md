# 📊 Text-to-SQL BI Dashboard

> **Chat with your database in plain English.** Powered by LangChain and the Groq API, this AI-driven Business Intelligence dashboard translates natural language questions into SQL queries, executes them live against an SQLite database, and automatically visualizes the results — no SQL knowledge required.

---

## 🚀 Live Demo

Ask questions like:
- *"Show me the total revenue by product category."*
- *"Which country has the most customers?"*
- *"What are the top 5 best-selling products?"*
- *"How many sales were made in January 2026?"*

The AI generates the SQL, runs it, returns the data table, and auto-generates an appropriate chart — all in seconds.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗣️ **Natural Language Interface** | Ask business questions in plain English |
| 🧠 **AI SQL Generation** | LangChain + Groq LLM translates English → SQL |
| 🔍 **SQL Transparency** | The generated SQL query is always shown to the user |
| 📋 **Interactive Data Table** | Results rendered as a scrollable, filterable dataframe |
| 📉 **Auto-Charting** | Automatically picks the best chart (Bar or Pie) for the data |
| 🔐 **Read-Only Safety** | SQL output is sanitized to prevent destructive queries |
| ⚡ **Multiple LLM Options** | Switch between Groq-hosted Llama 3.3, Llama 3.1, Mixtral, and Gemma2 |

---

## 🏗️ Architecture

```
User (Natural Language Question)
        │
        ▼
 ┌─────────────────────────────┐
 │   Streamlit Frontend (UI)   │
 │        app.py               │
 └────────────┬────────────────┘
              │
              ▼
 ┌─────────────────────────────┐
 │   SQL Agent  (sql_agent.py) │
 │  LangChain SQL Query Chain  │◄──── Groq API (LLM Brain)
 │  + Output Sanitization      │
 └────────────┬────────────────┘
              │  Cleaned SQL Query
              ▼
 ┌─────────────────────────────┐
 │   SQLite Database           │
 │   ecommerce.db              │
 └────────────┬────────────────┘
              │  Pandas DataFrame
              ▼
 ┌─────────────────────────────┐
 │   Plotly Express Charts     │
 │   Auto-generated visuals    │
 └─────────────────────────────┘
```

---

## 🗄️ Database Schema

The app uses a mock e-commerce SQLite database (`ecommerce.db`) with **3 tables** and **~400 rows** of realistic data:

**`Customers`** — 100 records across 6 countries (USA, Canada, UK, Australia, Germany, India)
| Column | Type | Description |
|---|---|---|
| `customer_id` | INTEGER PK | Unique identifier |
| `name` | TEXT | Customer name |
| `email` | TEXT | Email address |
| `country` | TEXT | Country of origin |
| `signup_date` | DATE | Account creation date |

**`Products`** — 8 products across 3 categories (Electronics, Furniture, Kitchen, Office Supplies)
| Column | Type | Description |
|---|---|---|
| `product_id` | INTEGER PK | Unique identifier |
| `product_name` | TEXT | Name of the product |
| `category` | TEXT | Product category |
| `price` | REAL | Unit price ($) |

**`Sales`** — 300 transactions spanning Dec 2025 – Mar 2026
| Column | Type | Description |
|---|---|---|
| `sale_id` | INTEGER PK | Unique identifier |
| `customer_id` | INTEGER FK | References `Customers` |
| `product_id` | INTEGER FK | References `Products` |
| `sale_date` | DATE | Date of sale |
| `quantity` | INTEGER | Units purchased |
| `total_amount` | REAL | Total value ($) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | [Streamlit](https://streamlit.io/) |
| **NLP → SQL Engine** | [LangChain](https://www.langchain.com/) (`create_sql_query_chain`) |
| **LLM Provider** | [Groq API](https://console.groq.com/) (ultra-fast inference) |
| **LLM Models** | Llama 3.3 70B, Llama 3.1 8B, Mixtral 8x7B, Gemma2 9B |
| **Database** | SQLite (via `langchain-community` SQLDatabase) |
| **Data Processing** | Pandas |
| **Visualization** | Plotly Express |

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.9+
- A free **Groq API Key** → [Get one here](https://console.groq.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/text-to-sql-bi-dashboard.git
cd text-to-sql-bi-dashboard
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

Run the database setup script once to generate the `ecommerce.db` file:

```bash
python database_setup.py
```

Expected output:
```
🛒 Building highly-realistic mock E-commerce Database...
✅ Database 'ecommerce.db' created successfully with 3 tables (Customers, Products, Sales).
```

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`. Enter your Groq API key in the sidebar and start asking questions!

---

## 🔑 Environment Variables (Optional)

You can pre-load your API key via a `.env` file instead of entering it in the sidebar each time:

```
# .env
GROQ_API_KEY=gsk_your_key_here
```

> ⚠️ **Never commit your `.env` file.** Add it to `.gitignore`.

---

## 📁 Project Structure

```
Text-to-SQL BI Dashboard/
│
├── app.py                 # Main Streamlit application & UI
├── sql_agent.py           # LangChain SQL chain, output sanitizer & query executor
├── database_setup.py      # Script to generate the mock SQLite database
├── ecommerce.db           # SQLite database (auto-generated)
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not committed)
└── README.md
```

---

## 🔒 Security

The SQL agent includes output sanitization to prevent misuse:

- SQL output is **cleaned of markdown formatting** (` ```sql ` blocks, backticks)
- **Conversational text** appended by small LLMs is stripped via regex
- Queries are **split on semicolons** — only the first statement executes, preventing SQL injection via chained commands (e.g., `; DROP TABLE ...`)
- The agent is designed for **read-only `SELECT` queries** in this context

---

## 🧠 How It Works

1. **User types** a natural language question into the chat input.
2. **LangChain's `create_sql_query_chain`** sends the question + database schema to the Groq-hosted LLM.
3. The LLM returns a **raw SQL query** (sometimes with extra formatting from smaller models).
4. The `sql_agent.py` **cleans and sanitizes** the SQL output.
5. **Pandas executes** the SQL against `ecommerce.db` via `sqlite3`.
6. The resulting **DataFrame** is displayed as a table in the UI.
7. **Plotly Express** auto-generates a Pie or Bar chart if the data shape supports it.

---

## 🗺️ Roadmap

- [ ] Support for user-uploaded databases (`.db`, `.csv`)
- [ ] Query history & bookmarking
- [ ] Multi-turn conversation memory
- [ ] Export results to CSV / Excel
- [ ] Deploy to Streamlit Community Cloud

---

## 👤 Author

**Girishwar** — [LinkedIn](https://linkedin.com/in/your-profile) · [GitHub](https://github.com/your-username)

---

## 📄 License

This project is licensed under the MIT License.
