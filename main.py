import functions

from chat import chat, FUNCTION_LOGGING
from colorama import init, Fore, Style
from multiprocessing import Process

PREAMBLE = """
You are an AI agent, more than a chat bot. You have access to many functions that you can call to help the user do certain things via tool calls.

Since you have so much power, make sure you're confident that the actions you are doing are correct. If you're unsure, prompt the user for more information.

These are some examples, not limited to, times when you should be extra careful to be correct:
1. If you're working with paths in the file directory, list the paths in the directory first to make sure your paths are correct.
2. If you're modifying a file, read the file first to make sure your modifications make sense.
"""


messages = [{"role": "system", "content": PREAMBLE}]

init()

def print_chat(prompt):
    messages.append({"role": "user", "content": prompt})
    for message_chunk in chat(messages):
        # Special log for running functions
        if message_chunk.startswith(FUNCTION_LOGGING + " "):
            print(f"{Fore.YELLOW}{message_chunk.split(FUNCTION_LOGGING)[1]}{Style.RESET_ALL}")
        else:
            print(message_chunk, end="")
    print()

while True:
    print_chat(input("You: "))
    # p = Process(target=chat, args=(prompt, messages))