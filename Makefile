.DEFAULT_GOAL := run
default: run

.PHONY: setup
setup:
	@echo "Compiling WhisperModel to CTranslate2"
	ct2-transformers-converter --model openai/whisper-base.en --output_dir whisper-base.en --quantization int16
	@echo "Installing Required Python Modules"
	pip install -r requirements.txt

.PHONY: run
run:
	python3 src/main.py


.PHONY: clean
clean:
	@echo "Removing Whisper Directory"
	rm -rf whisper-base.en