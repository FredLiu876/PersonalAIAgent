import functions
import json
import traceback

from client import client, GPT_MODEL

PREAMBLE = """
You are an AI agent. You have access to many functions that you can call to help the user do certain things via tool calls.

You also must follow some rules:
1. If a user asks for reading a file, double check the file path. Find the exact file path by listing files in the directory, then continue to list files in subdirectories where you think the file will be. If you can't find it, ask the user where the file is.
2. Before modifying, deleting or inserting a file, read the file first and follow the existing coding patterns in the file.
3. You can run any command in the terminal using run_bash_command.
4. Make sure to run non-interactive version of commands when using run_bash_command. Examples include using git --no-pager diff.
5. When using git, use git status, git branch and git diff before deciding to do anything with git. Afterwards, use git best principles, including writing meaningful git commits based on changes.
6. If you don't have the capability to do something or need to find something online, use online_search tool. This will give you a list of urls. Use read_text_from_url on those results and summarize the information
"""

FUNCTION_LOGGING = "FUNCTION_USE_ALERT"

def combine_tool_chunks(tool_chunks):
    def make_tool_object(tool_id, tool_function_name, tool_args):
        return {
            "id": tool_id,
            "type": "function",
            "function": {
                "name": tool_function_name,
                "arguments": tool_args
            }
        }
    tools = []
    current_tool_id = None
    current_tool_function_name = None
    current_tool_args = ""
    for chunk in tool_chunks:
        if chunk.id:
            if current_tool_id:
                tools.append(make_tool_object(current_tool_id, current_tool_function_name, current_tool_args))
            current_tool_function_name = chunk.function.name
            current_tool_id = chunk.id
            current_tool_args = ""
        current_tool_args += chunk.function.arguments
    if current_tool_id:
        tools.append(make_tool_object(current_tool_id, current_tool_function_name, current_tool_args))
    return tools


def chat(messages):
    stream = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        tools=functions.tools_dictionary,
        stream=True,
    )

    full_message = ""
    all_tool_chunks = []
    for chunk in stream:
        if chunk.choices[0].delta.content:
            message_chunk = chunk.choices[0].delta.content
            full_message += message_chunk
            yield message_chunk
        if chunk.choices[0].delta.tool_calls:
            all_tool_chunks += chunk.choices[0].delta.tool_calls
    if full_message:
        yield "\n"

    if all_tool_chunks:
        tools = combine_tool_chunks(all_tool_chunks)
        messages.append({
            "role": "assistant",
            "content": full_message if full_message else None,
            "tool_calls": tools,
        })

        for tool in tools:
            func_name = tool["function"]["name"]
            tool_response = f"Completed running {func_name}."
            try:
                arguments = json.loads(tool["function"]["arguments"])
                print_arguments = ""
                for k, v in arguments.items():
                    if type(v) == str:
                        if len(v) >= 100:
                            v = v[:100] + "..."
                    print_arguments += f"\n\t( {k}: {v} )"
                function_log = f"{FUNCTION_LOGGING} [ Running {func_name} with arguments {print_arguments} ]"
                yield function_log
                
                func = getattr(functions, func_name)
                func_result = func(**arguments)
                if func_result:
                    tool_response += "\n" + func_result
            except Exception as e:
                tool_response = f"There was an error running {func_name}.\n{traceback.format_exc()}"
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool["id"],
                "name": func_name,
                "content": tool_response,
            })

        for message_chunk in chat(messages):
            yield message_chunk
            full_message += message_chunk
    else:
        messages.append({"role": "assistant", "content": full_message})
