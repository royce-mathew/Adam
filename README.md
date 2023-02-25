# Installation
Install prerequirements for `adam`
```
pip install -r requirements.txt

```

Clone the Whisper model and convert it CTranslate2 format 
```
ct2-transformers-converter --model openai/whisper-base.en --output_dir whisper-base.en --quantization int16
```


## Performance compared to openai/whisper
The faster-whisper [github page](https://github.com/guillaumekln/faster-whisper) goes through this. Adam was also faster on faster-whisper compared to openai/whisper.

# TO-DO
Tasks that still need to be done.

- [ ]  Fix laggy audio input
- [ ]   Find synthetic voice synthesizer. 
    - espnet
    - wavenet_vocoder
    - neuml/txtai
- [ ]  Add commands folder / hook commands to assistant.py (similar to how discord.py handles its cogs)