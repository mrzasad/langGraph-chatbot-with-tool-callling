<img width="1207" height="528" alt="Screenshot 2026-05-25 020351" src="https://github.com/user-attachments/assets/3e4e4804-8add-438b-971a-aabfcf3b197d" />

# Target CRM – Complaint Management Chatbot

An AI-powered chatbot that automates customer complaint handling for **Target Superstore**. Built with **LangGraph**, **LangChain Tools**, and **Groq LLM**, the agent can search existing complaints and register new ones through natural conversation — eliminating manual lookups and data entry.

---

## Features

- **Natural Language Understanding** – Customers can ask: *"Check PK-88421"* or *"My order PK-99999 arrived damaged."*
- **Complaint Status Check** – Searches both processed complaints (approved/rejected) and pending complaints (awaiting review).
- **New Complaint Registration** – Inserts directly into the pending table with an automatic timestamp and 7-day TAT.
- **Smart Fallback Flow** – If a complaint is not found, the bot automatically offers to register a new one.
- **Tool-Calling LLM** – Uses Groq's `mixtral-8x7b-32768` with native function calling.
- **LangGraph Workflow** – Stateful agent with conditional routing between the LLM and tools.
- **Streamlit Chat UI** – Clean, responsive interface with persistent session history.
- **Bilingual Support** – Friendly, empathetic responses matching the customer's Urdu/English mix.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Chat UI | Streamlit |
| LLM Inference | Groq API (Mixtral / Llama) |
| Tool Definition | LangChain (`@tool` decorator) |
| Agent Orchestration | LangGraph (`StateGraph`) |
| Database | SQLite3 |
| Config | python-dotenv |

---

## Project Structure

```
complaint_chatbot/
├── .env                # API keys & model selection
├── requirements.txt    # Python dependencies
├── Target_crm.db       # SQLite database
├── db_helper.py        # Database operations (search & insert)
├── llm.py              # LLM initialisation (Groq/OpenAI)
├── tools.py            # LangChain tools (search, register)
├── agent.py            # LangGraph agent + system prompt
└── app.py              # Streamlit chat application
```

---

## Database Schema

**`user_complaint_processed`** – Complaints that have been reviewed.

| Column | Type | Description |
|---|---|---|
| tickets | INTEGER | Primary key |
| order_id | TEXT | Order identifier (e.g., PK-88421) |
| delivery_date | TEXT | Date product was delivered |
| claim_date | TEXT | Date complaint was filed |
| n_days_lapsed | INTEGER | Days between delivery and claim |
| decision | TEXT | APPROVED or REJECTED |
| reason | TEXT | Explanation of decision |

**`user_complaint_pending`** – Newly submitted complaints awaiting review.

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| order_id | TEXT | Order identifier |
| complaint_raw_text | TEXT | Customer's complaint description |
| created_at | TEXT | Auto-generated timestamp |

---

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768

# Optional – switch to OpenAI instead
# LLM_PROVIDER=openai
# OPENAI_API_KEY=your_openai_key
# OPENAI_MODEL=gpt-3.5-turbo
```

> **Supported models:** `mixtral-8x7b-32768`, `llama-3.1-8b-instant`, `gemma2-9b-it`

### 3. Prepare the database

Place `Target_crm.db` in the project root. If you don't have one, generate it with seed data:

```bash
# Set RUN_TESTS = True at the top of db_helper.py first
python db_helper.py
```

### 4. Run the chatbot

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## Example Conversations

| User Input | Bot Action |
|---|---|
| *"Check complaint PK-88421."* | Searches → returns APPROVED status with dates and reason. |
| *"Why was order PK-77109 rejected?"* | Searches → shows rejection reason (45 days lapsed, policy is 30 days). |
| *"My order PK-99999 arrived damaged."* | Searches → not found → *"No complaint found. Would you like to register one?"* |
| *"Yes, please register it."* | Calls register tool → confirms with 7-day resolution due date. |

---

## Architecture

The agent is built on a `StateGraph` with two nodes:

1. **LLM Node** – Receives the conversation and decides whether to call a tool or respond directly.
2. **Tools Node** – Executes `search_complaint_tool` or `register_pending_complaint_tool`.

A `tools_condition` edge routes back to the LLM after each tool call, allowing multi-step reasoning (e.g., search first, then offer registration if not found).

Conversation history is accumulated using LangGraph's `add_messages` reducer and persisted within the Streamlit session via `st.session_state`.

---

## Testing Without the UI

You can verify tool calling directly from the terminal:

```bash
python agent.py
```

```
You: Check PK-88421
Bot: ✅ Complaint found — APPROVED ...

You: Register PK-99999, product defective
Bot: ✅ Complaint registered. Expected resolution by ...
```

---

## Troubleshooting

**Model not found / decommissioned**

Update `GROQ_MODEL` in `.env` to a supported model such as `mixtral-8x7b-32768` or `llama-3.1-8b-instant`.

**Tool calls appear as raw `<function>` text**

The selected model may not support native function calling. Switch to one of the confirmed models above and ensure `langchain-groq>=0.2.0` is installed.

**Database errors**

Confirm `Target_crm.db` exists in the project root and is writable. Run `db_helper.py` to recreate and seed it.

**API key issues**

Check your key at [console.groq.com](https://console.groq.com) and confirm the selected model is available on your plan.





<img width="1017" height="222" alt="Screenshot 2026-05-23 224033" src="https://github.com/user-attachments/assets/10fdc895-afc3-4724-830b-99f86c088c77" />
<img width="1173" height="263" alt="Screenshot 2026-05-23 224021" src="https://github.com/user-attachments/assets/8ac0e5b9-0c01-48bb-b69d-68ec5afc060f" />
<img width="1206" height="252" alt="Screenshot 2026-05-23 224006" src="https://github.com/user-attachments/assets/d73f540e-6b57-4866-b62c-41593c1bddf2" />
<img width="1155" height="308" alt="Screenshot 2026-05-23 223956" src="https://github.com/user-attachments/assets/577c1249-f1b8-4b80-81d7-47e51faf6ffd" />
<img width="1326" height="291" alt="Screenshot 2026-05-23 223934" src="https://github.com/user-attachments/assets/6cd2dc41-4573-4edb-9ca1-c337c1e2d152" />
<img width="1146" height="598" alt="Screenshot 2026-05-23 224132" src="https://github.com/user-attachments/assets/325af1a2-481f-4504-9026-35b17d12a46e" />
<img width="1207" height="528" alt="Screenshot 2026-05-25 020351" src="https://github.com/user-attachments/assets/93bbe0b7-d460-45f5-874a-b86f2b887efe" />
