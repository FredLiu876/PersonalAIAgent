import streamlit as st

from agent import chat, FUNCTION_LOGGING, PREAMBLE

def format_function_style(text):
    return f"*:green[{text} ...]*"

def display_chat(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    user_message = st.chat_message("user")
    user_message.write(prompt)

    with st.spinner("Please wait..."):
        reply_chunk = []
        for message_chunk in chat(st.session_state.messages):
            # Special log for running functions
            if message_chunk.startswith(FUNCTION_LOGGING + " "):
                yield reply_chunk
                reply_chunk = []
                yield [format_function_style(message_chunk.split(FUNCTION_LOGGING)[1])]
            else:
                reply_chunk.append(message_chunk)
        yield reply_chunk

if __name__ == "__main__":
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": PREAMBLE}]

    for message in st.session_state.messages:
        # These are the messages that should be displayed
        if message["role"] in ["user", "assistant"]:
            with st.chat_message(message["role"]):
                if message["content"]:
                    st.write(message["content"])
                if "tool_calls" in message:
                    for tool in message["tool_calls"]:
                        st.write(format_function_style(f"[ Running {tool['function']['name']} ]"))
    
    prompt = st.chat_input("Prompt agent here")
    if prompt:
        for larger_chunk in display_chat(prompt):
            if larger_chunk:
                with st.chat_message("assistant"):
                    st.write_stream(larger_chunk)
        
    elif len(st.session_state.messages) == 1:
        st.write("Enter a prompt in the textbox below to begin chatting!")# Changes made according to user request
# Added and committed changes based on user request
