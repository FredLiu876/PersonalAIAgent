# Personal AI Agent

AI agent that will help you run things locally on your computer to assist with daily tasks!

## Running the app

There are two agents, description for each is further down the README.

To run the agents in the terminal, simply run

`python agent_terminal.py` or `python manager_terminal.py`

To run the agents in streamlit, simply run

`streamlit run Home.py`

and navigate to the corresponding pages.

#### Agent 🕵️‍♂️
The agent is a language model that can determine within your chat when to call functions to help you do things automatically!
You can ask it to edit files for you, ask about the weather today (which stumps all LLMs), etc.

Asking the agent about the weather:

https://github.com/FredLiu876/PersonalAIAgent/assets/48860751/74552417-19d0-4bf4-9c1b-a9c6fec9f71b


Asking the agent to make meaningful git commits for each file changed:

https://github.com/FredLiu876/PersonalAIAgent/assets/48860751/3120a1f6-5ca8-4b5c-8699-a28a729d31dd


- Works well with gpt-3.5-turbo

#### Manager 👨‍💼
The agent manager is very experimental: It is an additional language model that manages the agent, aiming to give you better results on broad tasks with minimal user input.
Asking the manager to make the agent figure out how to add a video component into streamlit in the correct place:


https://github.com/FredLiu876/PersonalAIAgent/assets/48860751/897734a9-5bb5-48ec-be46-5e6e963c9f33


Wasn't shown in the video, but the newly loaded streamlit UI looked like this, successfully with the weather today video!
![resulting_ui](https://github.com/FredLiu876/PersonalAIAgent/assets/48860751/7877ba1c-3b64-4508-ba26-e23dc467c102)

- If you use gpt-3.5-turbo, this is essentially a regular AI agent
- Works somewhat well with gpt-4-turbo
- Could use some fine-tuning to be even better!

### Adding new functions
If you want to integrate the agent into more parts, simply define a function within a python file within the functions folder. The functions.py will automatically pick up on this.

You must have the function follow this format:
- argument types annotated
- docstring with the description and the mandatory keyword `PARAMETERS DESCRIPTION:`

    - Each parameter is described by explaining it on the right side of the `->`
    - Parameter names in the docstring must match the parameter name defined in the function signature

```python
# Example Function

def new_function(input: str) -> str:
    """
    Description of the function for the LLM to understand what it does.

    PARAMETERS DESCRIPTION:
    input -> The input value.
    """
    # Function logic here
```
