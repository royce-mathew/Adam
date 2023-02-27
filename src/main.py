import os
import assistant;
import importlib
from colorama import Fore, Style

client = assistant.Assistant();

def main():
    print(f"{Fore.GREEN}Loading Modules{Fore.RESET}")
    for filename in os.listdir("./src/commands"):
        if filename.endswith(".py"):
            module_name = filename[:-3];
            try:
                module = importlib.import_module(f"commands.{module_name}")
                module.setup(client);
                print(f"Loaded {Fore.CYAN}{module_name}{Fore.RESET}")
            except Exception as e:
                print(f"Unable to laod command: {module_name}; Error: {e}")
                
                
    client.start()

if __name__ == "__main__":
    main();