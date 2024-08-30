import streamlit as st

st.write("### Welcome!")
st.write("🤚 to the Streamlit app for having conversations with your personal agents!")
st.write("Explore both of them by navigating to their respective pages in the left sidebar! Or read up on them below:")

agent, manager = st.tabs(["Agent 🕵️‍♂️", "Manager 👨‍💼"])
with agent:
    st.write("The agent is a language model that can determine within your chat when to call functions to help you do things automatically!")
    st.write("You can ask it to edit files for you, ask about the weather today (Which stumps all LLMs) etc.")
    st.write("The agent wrote the code, and the git commits themselves for many commits in this repository!")
    st.write("")
    st.write("Agent pulls most recent video from game bar into project:")
    st.video("assets/moving_most_recent_video.mp4")

with manager:
    st.warning("The agent manager is very experimental: It is an additional language model that manages the agent, in an attempt to give you better results on very broad tasks with minimal user input.")
    
    st.write("")
    st.write("Asking the agent to make meaningful git commits for each file changed:")
    st.video("assets/manager_instructs_agent_to_add_video.mp4")
    st.write("Not shown in the demo unfortunately, but the resulting ui successfully has the video added:")
    st.image("assets/resulting_ui.png")

    st.error("If you use gpt-3.5-turbo, this is essentially a regular AI agent")
    st.success("Works somewhat well with gpt-4-turbo")
    st.success("Could use some fine tuning to be even better!")