import streamlit as st

st.write("### Welcome!")
st.write("🤚 to the Streamlit app for having conversations with your personal agents!")
st.write("Explore both of them by navigating to their respective pages in the left sidebar! Or read up on them below:")
st.write("")
st.write("")

agent, manager = st.tabs(["Agent 🕵️‍♂️", "Manager 👨‍💼"])
with agent:
    st.write("The agent is a language model that can determine within your chat when to call functions to help you do things automatically!")
    st.write("You can ask it to edit files for you, etc.")
    st.write("")
    st.success("Works well with gpt-3.5-turbo")

with manager:
    st.warning("The agent manager is very experimental: It is an additional language model that manages the agent, in an attempt to give you better results on very broad tasks with minimal user input.")
    st.write("")
    st.error("It's essentially an agent with gpt-3.5-turbo")
    st.success("Works somewhat well with gpt-4-turbo")
    st.success("Could use some fine tuning to be even better!")
