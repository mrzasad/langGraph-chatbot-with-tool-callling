import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agent import build_agent

st.set_page_config(page_title="Imtiaz Complaint Assistant", page_icon="🤖")
st.title("🤖 Imtiaz CRM Complaint Assistant")
st.markdown("Ask about your complaint status or register a new issue.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = build_agent()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert to LangChain message format
    input_messages = []
    for m in st.session_state.messages:
        if m["role"] == "user":
            input_messages.append(HumanMessage(content=m["content"]))
        else:
            input_messages.append(AIMessage(content=m["content"]))

    try:
        # Invoke the agent
        result = st.session_state.agent.invoke({"messages": input_messages})
        last_message = result["messages"][-1]
        response = last_message.content if hasattr(last_message, "content") else str(last_message)
    except Exception as e:
        response = f"⚠️ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)