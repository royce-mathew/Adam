import os
import whisper
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wavefile

# Constants
MODEL = 'small'
FREQ_RANGE = [50, 1000] # Frequency to detect valid sounds
SAMPLE_RATE = 44100 # Stream device recording frequency
BLOCK_SIZE = 30 # Block size in milliseconds
THRESHOLD = 0.1 # Minimum volume threshold to activate listening
END_BLOCKS = 40 # Wait block for Whisper

class StreamHandler:
    def __init__(self, assistant=None):
        # Create a fake assistant if listener is being ran from main method
        if assistant is None:
            class fakeAssistant(): running, talking, analyze = True, False, None;
            self.assistant = fakeAssistant()
        else: self.assistant = assistant;
        
        self.running = True;
        self.padding = 0;
        self.prev_block = self.buffer = np.zeros((0, 1))
        self.file_ready = False

        print("Loading Model...")
        self.model = whisper.load_mode(f"{MODEL}.en")
        print("Loaded: [Model]")

    def callback(self, indata, frames, time, status):
        if not any(indata):
            print("\033[31m.\033[0m", end='', flush=True)
            return
        
        freq = np.argmax(np.abs(np.rfft(indata[:, 0]))) * SAMPLE_RATE / frames
        
        if np.sqrt(np.mean(indata ** 2)) > THRESHOLD and FREQ_RANGE[0] <= freq <= FREQ_RANGE[1] and not self.assistant.talking:
            print(".", end="", flush=True)
            if self.padding < 1: self.buffer = self.prevblock.copy()
            self.buffer = np.concatenate((self.buffer, self.indata))
            self.padding = END_BLOCKS
        else:
            self.padding -= 1
            if self.padding > 1:
                self.buffer = np.concatenate((self.buffer, indata))
            elif self.padding < 1 < self.buffer.shape[0] > SAMPLE_RATE: # If enough silence has passed, write to file
                self.fileready = True;
                wavefile.write("dictate.wav", SAMPLE_RATE, self.buffer)
                self.buffer = np.zeros((0, 1))
            elif self.padding < 1 < self.buffer.shape[0] < SAMPLE_RATE:
                self.buffer = np.zeros((0, 1))
                print("\033[2K\033[0G", end="", flush=True)
            else:
                self.prevblock = indata.copy()

    def process(self):
        if self.fileready:
            print("Transcribing")
            result = self.model.transcribe("dictate.wav", fp16=False, language="en", task="transcribe")
            print(f"Recieved Result: {result}")
            if self.assistant.analyze is not None: self.assistant.analyze(result["text"])
            self.fileread = False

    def listen(self):
        print("Listening")
        with sd.InputStream(channels=1, callback=self.callback, blocksize=int(SAMPLE_RATE * BLOCK_SIZE / 1000), samplerate=SAMPLE_RATE):
            while self.running and self.assistant.running: self.process();

def main():
    try:
        handler = StreamHandler();
        handler.listen()
    except (KeyboardInterrupt, SystemError): pass
    finally:
        if os.path.exists("dictate.wav"): os.remove("dictate.wav");
        print("Exited Program")

if __name__ == "__main__":
    main();