import streamlit as st

from agent import FUNCTION_LOGGING, PREAMBLE as AGENT_PREAMBLE
from manager import chat, PREAMBLE as MANAGER_PREAMBLE, AGENT_INDICATOR, MANAGER_INDICATOR, WORKER_PREFIX

def format_function_style(text):
    return f"*:green[{text} ...]*"

def display_chat(prompt):
    st.session_state.user_messages.append({"role": "user", "content": prompt})
    user_message = st.chat_message("user")
    user_message.write(prompt)

    reply_chunk = []
    for message_chunk in chat(st.session_state.user_messages, st.session_state.agent_manager_messages):
        # Special log for running functions
        if type(message_chunk) == int:
            yield reply_chunk
            reply_chunk = []
            yield message_chunk
            continue
            
        if message_chunk.startswith(FUNCTION_LOGGING + " "):
            yield reply_chunk
            reply_chunk = []
            yield [format_function_style(message_chunk.split(FUNCTION_LOGGING)[1])]
        else:
            reply_chunk.append(message_chunk)
    yield reply_chunk

if __name__ == "__main__":
    if "user_messages" not in st.session_state:
        st.session_state.user_messages = [{"role": "system", "content": MANAGER_PREAMBLE}]
        st.session_state.agent_manager_messages = [{"role": "system", "content": AGENT_PREAMBLE}]
    
    for message in st.session_state.user_messages:
        # These are the messages that should be displayed
        if message["role"] in ["user", "assistant"]:
            role = message["role"]
            if message["content"] is not None and WORKER_PREFIX in message["content"] and role == "user":
                role = "Worker"
            with st.chat_message(role):
                if message["content"]:
                    cut_content = message["content"]
                    if message["content"].startswith(WORKER_PREFIX) and role == "Worker":
                        cut_content = cut_content.split(WORKER_PREFIX, 1)[1]
                    st.write(cut_content)
                if "tool_calls" in message:
                    for tool in message["tool_calls"]:
                        st.write(format_function_style(tool['function']['name']))
    
    prompt = st.chat_input("Prompt agent here")
    if prompt:
        display_role = "assistant"
        for larger_chunk in display_chat(prompt):
            if type(larger_chunk) == int:
                if larger_chunk == MANAGER_INDICATOR:
                    display_role = "assistant"
                else:
                    display_role = "Worker"
            else:
                if larger_chunk:
                    with st.chat_message(display_role):
                        st.write_stream(larger_chunk)
    
    elif len(st.session_state.user_messages) == 1:
        st.write("Enter a prompt in the textbox below to begin chatting!")
