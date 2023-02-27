from listener import StreamHandler
import os, re
import pyttsx3

ASSISTANT_NAME = "adam"
# Makefile should install espeak

# Conversational Variables
# If a prompt without input has been initialized
init_convs =  [ASSISTANT_NAME, "hi", "okay", "ok", "hey"]
conv_starts = []
for v in init_convs:
    conv_starts.append([v, ASSISTANT_NAME] if v != ASSISTANT_NAME else [ASSISTANT_NAME])

class Assistant:
    def __init__(self):
        self.running = True
        self.talking = False
        self.prompted = False
        self.espeak = pyttsx3.init()
        self.espeak.setProperty('rate', 180) # speed of speech (Default is 175, 200 for pyttsx3)
        self.commands = [];

    def analyze(self, input):  # Decision tree for assistant
        string = "".join(ch for ch in input if ch not in ",.?!'").lower()  # Remove punctuations that Whisper adds
        query = string.split()  # Split into words

        if query in conv_starts: # if that's all they said, prompt for more input
            self.speak('Yes Sir, How can I help you?')
            self.prompted = True
        
        # Remove conversational starters from the query
        query = [word for word in query if word not in init_convs] # remake query without AIname prompts

        # Search the queried string with regex
        """
            for _, v in next, commands do
                -- check regex, if regex match
                    run()
                    break
                -- next
            end
        """

    def speak(self, text):
        self.talking = True
        print(f"\n\033[92m{text}\033[0m\n")
        self.espeak.say(text)
        self.espeak.runAndWait()
        self.talking = False

    def add_command(self, command_class):
        self.commands.append(command_class);

    def remove_command(self, command_class):
        self.commands.remove(command_class);

    def start(self):
        try:
            self.stream_handler = StreamHandler().listen()
        except (KeyboardInterrupt, SystemExit): pass
        finally:
            print("Exited")
            if os.path.exists('dictate.wav'): os.remove('dictate.wav')

if __name__ == '__main__':
    Assistant().start()