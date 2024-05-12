from agent import chat, FUNCTION_LOGGING, PREAMBLE
from colorama import init, Fore, Style
from multiprocessing import Process

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

if __name__ == "__main__":
    while True:
        print_chat(input("You: "))
        # p = Process(target=chat, args=(prompt, messages))