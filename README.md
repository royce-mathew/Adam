# Installation

Before running the makefile which automatically runs the setup for you, you need to have **Python** and **pip** already installed to your path.

To Install the Prerequisites for `adam` all you need to do is run the command

```
make setup
```
### Uninstallation
To remove and clean all packages installed by `adam`, run:
```
make clean
```
#  Running

Running the `make` command automatically runs the file for you. You need to be in the main directory to run the `make` command

```
make
```




##  Performance compared to openai/whisper

The faster-whisper [github page](https://github.com/guillaumekln/faster-whisper) goes through this. Adam was also faster on faster-whisper compared to openai/whisper.

#  TO-DO

Tasks that still need to be done.

- [x] Fix laggy audio input
- [x] Add commands folder / hook commands to assistant.py (similar to how discord.py handles its cogs)
- [ ] Find better way to hook functions; Find way to move `client.command` out of the init method.
- [ ] Add more commands, increase usability
- [ ] Find synthetic voice synthesizer.
- espnet
- wavenet_vocoder
- neuml/txtai
