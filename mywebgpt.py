import streamlit as st
import asyncio, httpx
from loguru import logger
from typing import Optional, List
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

# Use your Groq API key
API_KEY = os.getenv("GROQ_API_KEY")

# ================== Data Models ==================
class Message(BaseModel):
    role: str
    content: str

# ================== Groq Completion ==================
async def make_completion(messages: List[Message], nb_retries: int = 3, delay: int = 30) -> Optional[str]:
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    try:
        async with httpx.AsyncClient(headers=header, timeout=delay) as aio_client:
            counter = 0
            while counter < nb_retries:
                try:
                    resp = await aio_client.post(
                        url="https://api.groq.com/openai/v1/chat/completions",
                        json={
                            "model": "llama-3.3-70b-versatile",
                            "messages": [m.dict() for m in messages]  # for Pydantic v1
                        }
                    )
                    logger.debug(f"Status Code : {resp.status_code}")
                    if resp.status_code == 200:
                        return resp.json()["choices"][0]["message"]["content"]
                    else:
                        logger.warning(resp.content)
                        return None
                except Exception as e:
                    logger.error(e)
                    counter += 1
    except Exception as e:
        logger.error(f"Request failed: {e}")
    return None

# ================== Streamlit UI ==================
st.set_page_config(page_title="MiliBotz", page_icon="", layout="centered")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("You are chatting with **MiliBotz**, powered by Groq ")
    st.info(" Ask me anything! I can answer general or healthcare-related questions.")
    if st.button("Clear Chat"):
        st.session_state["history"] = []

# Title
st.markdown("<h1 style='text-align: center;'> Welcome to <span style='color: #4CAF50;'>MiliBotz</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Your AI assistant .</p>", unsafe_allow_html=True)

# Session state
if "history" not in st.session_state:
    st.session_state["history"] = []

if "input_key" not in st.session_state:
    st.session_state["input_key"] = 0   # to reset text_input

# Display messages WhatsApp style
for msg in st.session_state["history"]:
    if msg.role == "user":
        st.markdown(
            f"<div style='text-align: right; background-color: #dcf8c6; color: black; padding: 10px; border-radius: 10px; margin: 5px 0; display: inline-block; max-width: 80%; float: right;'>{msg.content}</div><div style='clear: both;'></div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align: left; background-color: #ffffff; color: black; padding: 10px; border-radius: 10px; margin: 5px 0; display: inline-block; max-width: 80%; float: left;'>{msg.content}</div><div style='clear: both;'></div>",
            unsafe_allow_html=True
        )

# Input at bottom
st.markdown("---")
user_input = st.text_input(" Type your message:", key=f"input_{st.session_state['input_key']}")

if st.button("Send") and user_input.strip():
    st.session_state["history"].append(Message(role="user", content=user_input))

    # Get bot reply
    response = asyncio.run(make_completion(st.session_state["history"]))
    if response is None:
        response = " Sorry, I couldn’t fetch a reply. Try again!"
    st.session_state["history"].append(Message(role="assistant", content=response))

    # increment key → this clears the text box
    st.session_state["input_key"] += 1

    st.rerun()
