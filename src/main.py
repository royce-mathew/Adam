import os
import assistant;
import importlib
from colorama import Fore, Style

# Create a new assistant
client = assistant.Assistant();

def main():
    print(f"{Fore.GREEN}Loading Modules{Fore.RESET}")
    for filename in os.listdir("./src/commands"): # Load modules
        if filename.endswith(".py"):
            module_name = filename[:-3];
            try:
                module = importlib.import_module(f"commands.{module_name}") # Import module
                module.setup(client); # Run setup command
                print(f"Loaded {Fore.CYAN}{module_name}{Fore.RESET}")
            except Exception as e:
                print(f"Unable to laod command: {module_name}; Error: {e}")
                
    client.start()

if __name__ == "__main__":
    main();