from client import client, GPT_MODEL
from agent import chat as agent_chat, FUNCTION_LOGGING

WORKER_PREFIX = "Worker: "
MANAGER_INDICATOR = 0
AGENT_INDICATOR = 1

PREAMBLE = f"""
Your task is to instruct your worker to do the things users ask of you.
To use your worker, prefix your message with "{WORKER_PREFIX}" and follow up with instructions for the worker. All non-prefixed messages are assumed to go back to the user. The worker will report back after each of these tasks with "{WORKER_PREFIX}".
Just make sure to wait for the worker's reply before giving him a new task. You can also ask him for clarifications on how he did each task.

For example, to write new code based on documentation, you can do:
{WORKER_PREFIX} read the documentation at this website https://docs.github.com/en/actions/using-workflows/about-workflows

{WORKER_PREFIX} use that documentation to edit .github/workflows/workflow.yml

After the worker replies, double check that the worker did things correctly. Ask questions like:
{WORKER_PREFIX} read the file .github/workflows/workflow.yml and verify that all changes were correctly made

If the worker replies with an issue, tell it to fix it. If the worker says everything is still correct, hand it back to the user.


This is another example of a conversation.
Remember that messages prefixed with "{WORKER_PREFIX}" is a conversation between you and the worker, and anything not prefixed is a conversation between you and the user.

User asks for: Create a new streamlit frontend interface that displays the conversation in manager.py
You will instruct the worker: {WORKER_PREFIX} read manager.py and tell me what it does
User replies as the worker: {WORKER_PREFIX} I have read manager.py. It consists of a chatbot that instructs an agent to do work
You will continue to instruct the worker: {WORKER_PREFIX} Create an app.py that displays each message
User replies as the worker: {WORKER_PREFIX} I have created a file named app.py and built a simple interface to show each message in the chatHistory!
You ask the worker to double check: {WORKER_PREFIX} Double check this work and fill in any templated code.
User replies as the worker: {WORKER_PREFIX} Yes, the interface is nice and clean and makes use of textfields.
You prompt the user again: The streamlit app has been made, is there anything else you would like me to do?
User says: That's all, thank you!

The worker makes many mistakes, but if you ask it to double check, it will often correct itself.
Always make sure that after you receive a reply from the worker prefixed with {WORKER_PREFIX}, ask the worker to double check its work before handing it back to the user.

Remember to instruct your worker to do anything.
"""

def chat(user_messages, agent_manager_messages):
    while True:
        stream = client.chat.completions.create(
            model=GPT_MODEL,
            messages=user_messages,
            stream=True,
        )

        yield MANAGER_INDICATOR
        full_message = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                message_chunk = chunk.choices[0].delta.content
                full_message += message_chunk
                yield message_chunk
        yield "\n"

        if WORKER_PREFIX in full_message:
            user_messages.append({"role": "assistant", "content": full_message})
            agent_manager_messages.append({"role": "user", "content": full_message})
            
            agent_full_message = ""
            yield AGENT_INDICATOR
            for agent_message_chunk in agent_chat(agent_manager_messages):
                if not agent_message_chunk.startswith(FUNCTION_LOGGING + " "):
                    agent_full_message += agent_message_chunk
                yield agent_message_chunk
            yield "\n"
            
            user_messages.append({"role": "user", "content": WORKER_PREFIX + agent_full_message})

        else:
            user_messages.append({"role": "assistant", "content": full_message})
            break


    