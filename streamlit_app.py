import streamlit as st
import openai
import os

# Initialize the OpenAI API client
openai.api_key = st.secrets["OPENAI"]

def generate_code_chat(messages):
    """
    Generate code using ChatGPT based on the provided messages.

    Parameters:
    messages (list): The chat history messages.

    Returns:
    str: The generated code.
    """
    response = openai.ChatCompletion.create(
        model=st.secrets["model"],
        messages=messages,
        max_tokens=2048,
        temperature=0.5
    )
    return response['choices'][0]['message']['content'].strip()

# Streamlit Interface
st.set_page_config(layout="wide")

# Sidebar for language selection
with st.sidebar:
    st.title("Code Assistant")
    st.caption("Ramsurrun Nadish")
    
    # Language Selection
    languages = ["Python", "Rust", "Ruby", "C#", "Julia", "Bash", "TypeScript", "Go", "Java", "Neo4j Cypher", "C++", "SQL", "JavaScript"]
    language = st.selectbox("Select Programming Language", languages)
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": f"You are an expert {language} programmer. Provide detailed, well-commented, and efficient code solutions. Always include necessary imports and explanations for complex sections."},
        {"role": "assistant", "content": f"I am your expert {language} coding assistant. How can I help you with {language} coding today?"}
    ]
else:
    # Check if the language has changed
    if st.session_state.get("selected_language") != language:
        st.session_state["messages"] = [
            {"role": "system", "content": f"You are an expert {language} programmer. Provide detailed, well-commented, and efficient code solutions. Always include necessary imports and explanations for complex sections."},
            {"role": "assistant", "content": f"I am your expert {language} coding assistant. How can I help you with {language} coding today?"}
        ]
    st.session_state["selected_language"] = language

# Display chat history (latest chat at the bottom)
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(f"**You:** {msg['content']}")
        else:
            st.chat_message("assistant").write(f"**Assistant:** {msg['content']}")

# Input field
prompt = st.chat_input("Type your message here...")

# Process input
if prompt:
    if not openai.api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    generated_code = generate_code_chat(st.session_state.messages)
    
    # Add assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": generated_code})
    
    # Rerun to update chat
    st.experimental_rerun()
