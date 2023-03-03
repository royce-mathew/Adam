import os
from faster_whisper import WhisperModel
import numpy as np
import sounddevice as sd
import soundfile as sf
from colorama import Fore, Style
from typing import Optional, Tuple, Callable
from scipy.io import wavfile
import io

# SETTINGS
MODEL_PATH: str = f"whisper-base.en/"
ENGLISH_ONLY: bool = True # English only model
ECHO: bool = False # Hear your own voice for debugging
INPUT_DEVICE: Optional[Tuple[int, int]] = None# (4, 4) # [Input_ID, Output_ID] You can check this with sd.query_devices()
FREQ_RANGE: Tuple[int, int] = (50, 1000) # Frequency to detect valid sounds 
SAMPLE_RATE: int = 44100 # Stream device recording frequency
BLOCK_SIZE: int = 30 # Block size in milliseconds
THRESHOLD: float = 0.1 # Minimum volume threshold to activate listening
END_BLOCKS: int = 30 # Wait block for Whisper


# CONSTANTS
NP_ZEROS = np.zeros((0, 1))

# Create a fake assistant if listener is being ran as main for testing
class fakeAssistant(): 
    running: bool = True
    talking: bool = False
    analyze: Optional[Callable] = None

class StreamHandler:
    def __init__(self, assistant=fakeAssistant()):
        self.assistant = assistant
        self.padding: int = 0
        self.running: bool = True
        self.audio_ready: bool = False
        self.buffer: np.ndarray = NP_ZEROS
        self.prev_block: np.ndarray = NP_ZEROS
        self.audio: np.ndarray = NP_ZEROS
        sd.default.device = INPUT_DEVICE or sd.default.device # type: ignore
        print(f"Using Audio Device: {Style.BRIGHT}{Fore.GREEN}{sd.default.device}")
        self.model: WhisperModel = WhisperModel(MODEL_PATH, device="cpu", compute_type="int8")
        print(Style.BRIGHT + Fore.BLUE + "Loaded Model" + Style.RESET_ALL)


    def callback(self, indata: np.ndarray, frames: int, time, status: sd.CallbackFlags) -> None:
        if not any(indata):
            raise Exception(Style.BRIGHT + Fore.RED + "No Input Recieved. Is your 'INPUT_DEVICE' Correct?" + Style.RESET_ALL)
        
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
                
                # wavfile.write("dictate.wav", SAMPLE_RATE, self.buffer)
                self.audio = self.buffer.copy();
                self.buffer = NP_ZEROS
                self.audio_ready = True
            
            elif self.padding < 1 < self.buffer.shape[0] < SAMPLE_RATE:
                self.buffer = NP_ZEROS
            else:
                self.prev_block = indata.copy()


    def process(self):
        if self.audio_ready:
            # Convert audio to io file
            # import time;
            # init_time = time.time()

            bytes_wav = bytes()
            bytes_io = io.BytesIO(bytes_wav)
            wavfile.write(bytes_io, rate=SAMPLE_RATE, data=self.audio)

            # print(self.audio)
            segments, info = self.model.transcribe(bytes_io, language="en", beam_size=3)
            result: str = "".join(x.text for x in segments)
            # print(time.time() - init_time)
            print(f"{Style.BRIGHT}{Fore.BLUE}Recieved Result:{Style.RESET_ALL} {result}")
            if self.assistant.analyze is not None: self.assistant.analyze(result)
            self.audio_ready = False


    def listen(self) -> None:
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
