import os
from faster_whisper import WhisperModel
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wavfile
import threading
from colorama import Fore, Style
from typing import Optional, Tuple

# SETTINGS
MODEL_PATH: str = "whisper-base.en/"
ENGLISH_ONLY: str = True # English only model
ECHO: str = False # Hear your own voice for debugging
INPUT_DEVICE: Tuple[int, int] = (5, 4) # [Input_ID, Output_ID] You can check this with sd.query_devices()
FREQ_RANGE: Tuple[int, int] = (50, 1000) # Frequency to detect valid sounds 
SAMPLE_RATE: int = 44100 # Stream device recording frequency
BLOCK_SIZE: int = 30 # Block size in milliseconds
THRESHOLD: float = 0.08 # Minimum volume threshold to activate listening
END_BLOCKS: int = 40 # Wait block for Whisper


# CONSTANTS
NP_ZEROS = np.zeros((0, 1))

class StreamHandler:
    def __init__(self, assistant=None):
        # Create a fake assistant if listener is being ran from main method
        if assistant is None:
            class fakeAssistant(): 
                running: bool = True
                talking: bool = False
                analyze: Optional[callable] = None
            self.assistant = fakeAssistant()
        else: self.assistant = assistant;
        
        self.running: bool = True
        self.padding: int = 0
        self.prev_block = self.buffer = NP_ZEROS
        self.file_ready: bool = False
        sd.default.device = INPUT_DEVICE or sd.default.device

        print(f"Using Audio Device: {Style.BRIGHT}{Fore.GREEN}{sd.default.device}")
        self.model: WhisperModel = WhisperModel(MODEL_PATH, device="cpu", compute_type="int8")
        print(Style.BRIGHT + Fore.BLUE + "Loaded Model" + Style.RESET_ALL)


    def callback(self, indata: np.ndarray, frames: int, time, status: sd.CallbackFlags):
        if not any(indata):
            raise Exception(Style.BRIGHT + Fore.RED + "No Input Recieved. Is your 'INPUT_DEVICE' Correct?" + Style.RESET_ALL)
        
        # fft_abs = np.abs(np.fft.rfft(indata[:, 0]))
        # freq: float = np.argmax(fft_abs) * SAMPLE_RATE / frames
        
        # if np.sqrt(np.mean(indata ** 2)) > THRESHOLD and FREQ_RANGE[0] <= freq <= FREQ_RANGE[1]
        if indata.max() > THRESHOLD and not self.assistant.talking:
            if self.padding < 1: self.buffer = self.prev_block.copy()
            self.buffer = np.concatenate((self.buffer, indata))
            self.padding = END_BLOCKS
        else:
            self.padding -= 1
            if self.padding > 1:
                self.buffer = np.concatenate((self.buffer, indata))
            
            elif self.padding < 1 < self.buffer.shape[0] > SAMPLE_RATE: # If enough silence has passed, write to file
                if ECHO:
                    self.assistant.talking = True
                    sd.play(self.buffer, SAMPLE_RATE)
                    sd.wait()
                    self.assistant.talking = False
                
                wavfile.write("dictate.wav", SAMPLE_RATE, self.buffer)
                self.buffer = NP_ZEROS
                self.file_ready = True
            
            elif self.padding < 1 < self.buffer.shape[0] < SAMPLE_RATE:
                self.buffer = NP_ZEROS
            else:
                self.prev_block = indata.copy()


    def process(self):
        if self.file_ready:
            segments, info = self.model.transcribe("dictate.wav")
            result: str = ""
            for s in segments:
                result += s.text
            print(f"{Style.BRIGHT + Fore.BLUE}Recieved Result:{Style.RESET_ALL} {result}")
            if self.assistant.analyze != None: self.assistant.analyze(result)
            self.file_ready = False


    def listen(self):
        print(Style.BRIGHT + Fore.GREEN + "Listening" + Style.RESET_ALL)
        with sd.InputStream(channels=1, callback=self.callback, blocksize=int(SAMPLE_RATE * BLOCK_SIZE / 1000), samplerate=SAMPLE_RATE):
            while self.running and self.assistant.running: self.process();


def main():
    try:
        handler = StreamHandler()
        handler.listen()
    except (KeyboardInterrupt, SystemExit): pass
    finally:
        if os.path.exists("dictate.wav"): os.remove("dictate.wav");
        print("Exited Program")

if __name__ == "__main__":
    main()
