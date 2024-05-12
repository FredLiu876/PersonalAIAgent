# Personal AI Agent

AI agent that will help you run things locally on your computer to assist with daily tasks!

#### Agent 🕵️‍♂️
The agent is a language model that can determine within your chat when to call functions to help you do things automatically!
You can ask it to edit files for you, ask about the weather today (which stumps all LLMs), etc.

Asking the agent about the weather:
![Weather Video](weather_today.mp4)

Asking the agent to make meaningful git commits for each file changed:
![Git Commit Video](making_meaningful_git_commits_for_each_file.mp4)
- Works well with gpt-3.5-turbo

#### Manager 👨‍💼
The agent manager is very experimental: It is an additional language model that manages the agent, aiming to give you better results on broad tasks with minimal user input.

Asking the agent to make meaningful git commits for each file changed:
![Manager Instructing Agent Video](manager_instructs_agent_to_add_video.mp4)
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
