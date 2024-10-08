# Personal AI Agent

AI agent that will help you run things locally on your computer to assist with daily tasks! Once the agent was setup with barebones functions to code and modify files, a lot of the other code was easily written and committed using the agent itself. Very fast development for small projects!

## Setup

You'll need an OpenAI API key. Run the `setup.sh OPENAI_API_KEY_HERE` script to configure it and create the secrets file for you.

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
Many of the commits were written entirely by the agent (including the git commands themselves)

https://github.com/user-attachments/assets/aee0349d-671d-4f93-aa83-d9b48a610aea

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

## Running Unit Tests

To run the unit tests for the project, follow these steps:

1. Navigate to the project directory where the `unit_tests` folder is located.
2. Run the following command in your terminal:
   
   ```bash
   python -m unittest discover -s unit_tests
   ```

This command will discover and execute all unit tests located in the `unit_tests` directory.
