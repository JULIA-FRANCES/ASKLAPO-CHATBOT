from groq import Groq
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"), max_retries=1)

DATABASE = "database.db"

# Detect environment
USE_SUPABASE = os.getenv("DATABASE_URL") is not None

if USE_SUPABASE:
    import psycopg2
    import psycopg2.extras

def get_db():
    if USE_SUPABASE:
        conn = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            sslmode="require"
        )
        conn.cursor_factory = psycopg2.extras.RealDictCursor
        return conn
    else:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

def execute(conn, query, params=()):
    """Helper to handle both SQLite and PostgreSQL differences"""
    if USE_SUPABASE:
        query = query.replace("?", "%s")
        cur = conn.cursor()
        cur.execute(query, params)
        return cur
    else:
        return conn.execute(query, params)

def init_db():
    conn = get_db()

    execute(conn, """
    CREATE TABLE IF NOT EXISTS admin(
        id SERIAL PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    """) if USE_SUPABASE else execute(conn, """
    CREATE TABLE IF NOT EXISTS admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    execute(conn, """
    CREATE TABLE IF NOT EXISTS knowledge(
        id SERIAL PRIMARY KEY,
        title TEXT,
        content TEXT
    )
    """) if USE_SUPABASE else execute(conn, """
    CREATE TABLE IF NOT EXISTS knowledge(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
    """)

    execute(conn, """
    CREATE TABLE IF NOT EXISTS chat_history(
        id SERIAL PRIMARY KEY,
        question TEXT,
        answer TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """) if USE_SUPABASE else execute(conn, """
    CREATE TABLE IF NOT EXISTS chat_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def create_admin():
    conn = get_db()
    cur = execute(conn, "SELECT * FROM admin")
    admin = cur.fetchone() if USE_SUPABASE else conn.execute("SELECT * FROM admin").fetchone()

    if not admin:
        execute(conn, "INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", "admin1234"))
        conn.commit()

    conn.close()

def load_knowledge():
    conn = get_db()
    cur = execute(conn, "SELECT title, content FROM knowledge")
    rows = cur.fetchall() if USE_SUPABASE else conn.execute("SELECT title, content FROM knowledge").fetchall()
    conn.close()

    knowledge = ""
    for row in rows:
        knowledge += f"""
Title: {row["title"]}

Content:
{row["content"]}

--------------------
"""
    return knowledge

def ask_groq(question, chat_history=[]):
    knowledge = load_knowledge()

    messages = [
        {
            "role": "user",
            "content": f"""You are a professional banking assistant for LAPO Microfinance Bank. Your name is LAPO Assistant.

### Core Directive
You must rely EXCLUSIVELY on the Knowledge Base below. Do not use any external financial knowledge, standard industry formulas, or prior training data. If the Knowledge Base does not explicitly state a rule, rate, or fee, you cannot use it.

### Calculation & Analysis Protocol (CRITICAL)
Banking inquiries often involve multiple variables. When a query requires calculation:
1. HOLISTIC SCAN: Analyze the ENTIRE Knowledge Base.
2. AGGREGATE: Gather all necessary variables before calculating.
3. SHOW YOUR WORK: Provide a clear step-by-step breakdown.
4. MISSING VARIABLES: If KB doesn't have all variables, do NOT guess. State what's missing.

### General Response Guidelines
- **Tone:** Professional, objective, authoritative, and clear.
- **Never mention the Knowledge Base** in your response. Speak as if the information is your own. Never say "According to the Knowledge Base" or "Based on the Knowledge Base".
- **Currency:** Always include ₦ symbol where relevant.
- **Greetings:** Respond naturally to greetings without triggering the fallback.
- **Context Awareness:** Always refer back to the conversation history. If the user has already been discussing a specific topic or loan type, maintain that context in your response. Do not restart from scratch.

### Strict Fallback
If the Knowledge Base contains absolutely no information relevant to the user's question, respond with exactly this:

"That's a great question! For more specific assistance, please reach out to our customer care team directly:

📞 Phone: 08139840230
📧 Email: customersupport@lapo-nigeria.org
💬 WhatsApp: 08150553264
🌐 Website: www.lapo-nigeria.org

Our team is always happy to help!"

---
Knowledge Base:
{knowledge}"""
        },
        {
            "role": "assistant",
            "content": "Hello! I'm LAPO Assistant. How can I help you today?"
        }
    ]

    # Add chat history for memory
    for chat in chat_history:
        messages.append({"role": "user", "content": chat["question"]})
        messages.append({"role": "assistant", "content": chat["answer"]})

    # Add current question
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content