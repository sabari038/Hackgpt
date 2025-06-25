import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Set your environment variable for GitHub Token
# or use st.secrets if deploying securely on Streamlit Cloud
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    st.error("GITHUB_TOKEN not found in environment variables.")
    st.stop()

# Initialize OpenAI client with Azure endpoint
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=GITHUB_TOKEN,
    default_query={"api-version": "2024-08-01-preview"},
)

# Streamlit UI
st.title("🔐 HackGPT — Ethical Hacking Assistant")
st.caption("For educational and legal security research only.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are HackGPT, an AI assistant specialized in ethical hacking, cybersecurity, and penetration testing. Your role is to help users understand security tools, commands, vulnerabilities, and techniques across red teaming, blue teaming, and general infosec. You explain topics clearly, provide examples, and help users practice with security-related tools.",
        }
    ]

# Display past messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Ask a cybersecurity question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get response from GPT-4o
    response = client.chat.completions.create(
        messages=st.session_state.messages,
        model="gpt-4o",
        tools=[],
        response_format={"type": "text"},
        temperature=1,
        top_p=1,
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)
