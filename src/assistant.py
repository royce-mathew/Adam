from listener import StreamHandler
from typing import Callable, Optional
from colorama import Fore
import os, re
import pyttsx3

# Constants
ASSISTANT_NAME = "Adam"
ASSISTANT_LOWER = ASSISTANT_NAME.lower()

# Conversational Variables
# If a prompt without input has been initialized
init_convs: list =  [ASSISTANT_LOWER, "hi", "okay", "ok", "hey"]
conv_ends: list = ["stop", "alright", "thanks"]
conv_starts: list = []
for v in init_convs:
    conv_starts.append([v, ASSISTANT_LOWER] if v != ASSISTANT_LOWER else [ASSISTANT_LOWER])


class Assistant:
    def __init__(self):
        self.running: bool = True
        self.talking: bool = False
        self.prompted: bool = False
        self.espeak: pyttsx3.Engine = pyttsx3.init()
        self.espeak.setProperty('rate', 180) # speed of speech (Default is 175, 200 for pyttsx3)
        self.classes: list = []
        self.commands: dict = {}

    def analyze(self, input) -> None:  # Decision tree for assistant
        str_query: str = "".join(ch for ch in input if ch not in ",.?!'").lower()  # Remove punctuations that Whisper adds
        query: list[str] = str_query.split()  # Split into words

        if query in conv_starts: # Start prompt for more input
            self.speak('Yes Sir, How can I help you?')
            self.prompted = True
            return
        
        if not self.prompted: return; # If bot was not prompted
    
        if query in conv_ends: # Conversation ended
            self.speak('Alright sir, have a good day!')
            self.prompted = False
            return

        # Remove conversational starters from the query
        query = [word for word in query if word not in init_convs] # remake query without AIname prompts

        str_query = " ".join(query) # Convert to string
        for command_regex, command in self.commands.items():
            if re.search(command_regex, str_query):
                command(query)
                self.prompted = False
                break


    def speak(self, text: str) -> None:
        print(f"{Fore.GREEN}{ASSISTANT_LOWER}{Fore.RESET}: {text}")
        self.talking = True
        self.espeak.say(text)
        self.espeak.runAndWait()
        self.talking = False


    def command(self, regex: str) -> Callable:
        def add_command(function) -> Callable:
            self.commands[regex] = function
            def wrapper(*args, **kwargs) -> Callable:
                return function(*args, **kwargs)
            return wrapper
        return add_command
    
    def run_command(self, regex: str, query: Optional[list[str]] = None) -> None:
        try:
            self.commands[regex](query) # Try running the command with the passed regex
        except Exception as err:
            print(f"{Fore.RED}An Error Occurred:{Fore.RESET} {err}")


    def add_class(self, command_class) -> None:
        self.classes.append(command_class);

    def remove_class(self, command_class) -> None:
        self.classes.remove(command_class);

    def start(self) -> None:
        try:
            self.stream_handler = StreamHandler(assistant=self).listen() # type: ignore
        except (KeyboardInterrupt, SystemExit): pass
        finally:
            print("Exited")