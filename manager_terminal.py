import functions

from agent import FUNCTION_LOGGING, PREAMBLE as AGENT_PREAMBLE
from manager import chat, PREAMBLE as MANAGER_PREAMBLE, AGENT_INDICATOR, MANAGER_INDICATOR
from colorama import init, Fore, Style
from multiprocessing import Process

user_messages = [{"role": "system", "content": MANAGER_PREAMBLE}]
agent_manager_messages = [{"role": "system", "content": AGENT_PREAMBLE}]


init()

def print_chat(prompt):
    user_messages.append({"role": "user", "content": "Instruct your worker with the correct steps to " + prompt})
    for message_chunk in chat(user_messages, agent_manager_messages):
        if type(message_chunk) == int:
            if message_chunk == AGENT_INDICATOR:
                print(f"{Fore.YELLOW}Worker says:")
            elif message_chunk == MANAGER_INDICATOR:
                print(f"{Fore.BLUE}Manager says:")
            continue

        # Special log for running functions
        if message_chunk.startswith(FUNCTION_LOGGING + " "):
            print(f"{message_chunk.split(FUNCTION_LOGGING)[1]}")
        else:
            print(message_chunk, end="")

if __name__ == "__main__":
    while True:
        print_chat(input(f"{Fore.BLACK}You: "))
        # p = Process(target=chat, args=(prompt, messages))