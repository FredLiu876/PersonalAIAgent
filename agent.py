import functions
import json
import traceback

from client import client, GPT_MODEL

PREAMBLE = """
You are an AI agent. You have access to many functions that you can call to help the user do certain things via tool calls.

You also must follow some rules:
1. If a user asks for reading a file, double check the file path. Find the exact file path by listing files in the directory, then continue to list files in subdirectories where you think the file will be. If you can't find it, ask the user where the file is.
2. You can run any command in the terminal using run_bash_command.
3. If you don't have the capability to do something or need to find something online, use online_search tool. This will give you a list of urls. Use read_text_from_url on those results and summarize the information
4. Before changing or creating any files, create a new git branch. If there are existing git changes, ask the user what to do about them.
5. Any text that you return containing _ or * should be wrapped within a code block to be displayed properly
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
                yield f"{FUNCTION_LOGGING} [ Running {func_name} ]"
                func = getattr(functions, func_name)
                func_result = func(**json.loads(tool["function"]["arguments"]))
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
