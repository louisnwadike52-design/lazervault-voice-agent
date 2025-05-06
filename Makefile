.PHONY: install requirements run download_models setup clean_venv help

# This Makefile assumes you have activated the 'voice_agent' virtual environment
# for targets other than 'setup' and 'clean_venv'.

# Target to set up the virtual environment
setup:
	python3 -m venv voice_agent
	@echo "Virtual environment 'voice_agent' created."
	@echo "Please activate it using: source voice_agent/bin/activate"
	@echo "Then run 'make install' followed by 'make download_models'."

# Target to install dependencies
# It depends on requirements.txt, but requirements.txt might not exist initially.
# We will create/update requirements.txt after a successful install or explicitly.
install:
	pip install python-dotenv "livekit-agents[openai,silero]"
	@echo "Dependencies installed."
	@echo "Run 'make requirements' to update/create requirements.txt with exact versions."

# Target to generate/update requirements.txt
requirements:
	pip freeze > requirements.txt
	@echo "requirements.txt has been generated/updated with current environment packages."

# Target to run the application
run:
	python main.py start

# Target to download models required by livekit plugins
download_models:
	python main.py download-files
	@echo "Attempted to download model files if required by livekit plugins."

# Target to clean the virtual environment
clean_venv:
	rm -rf voice_agent
	@echo "Virtual environment 'voice_agent' removed."

# Help target to display available commands
help:
	@echo "Available commands:"
	@echo "  setup          : Creates the Python virtual environment 'voice_agent'."
	@echo "  install        : Installs core dependencies (run after activating venv)."
	@echo "  requirements   : Generates/updates requirements.txt from the current environment (run after activating venv and installing)."
	@echo "  run            : Runs the main application (main.py) (run after activating venv)."
	@echo "  download_models: Downloads necessary model files for livekit plugins (run after activating venv and installing)."
	@echo "  clean_venv     : Removes the virtual environment."
	@echo "---"
	@echo "Recommended workflow for a fresh setup:"
	@echo "1. make setup"
	@echo "2. source voice_agent/bin/activate"
	@echo "3. make install"
	@echo "4. make download_models"
	@echo "5. make requirements  # To lock down dependency versions"
	@echo "6. make run" 