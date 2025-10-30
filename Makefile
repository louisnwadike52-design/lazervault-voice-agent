.PHONY: help install run shell migrate requirements deploy

# Variables
PYTHON = python
PIP = pip
ACTIVATE = . voice_agent/bin/activate &&
MANAGE = $(ACTIVATE) $(PYTHON) manage.py

# Get the current timestamp for versioning
VERSION := $(shell date +%Y%m%d-%H%M%S)
IMAGE_NAME := europe-west1-docker.pkg.dev/juicy-odds/voice/voice-agent

help:
	@echo "Available commands:"
	@echo "  requirements - Freeze dependencies into requirements.txt"
	@echo "  install      - Install dependencies from requirements.txt"
	@echo "  migrate      - Run database migrations"
	@echo "  run          - Run the Django development server"
	@echo "  shell        - Start a new shell with the venv activated"
	@echo "  deploy       - Deploy to App Engine"

requirements:
	$(ACTIVATE) $(PIP) freeze > requirements.txt
	@echo "requirements.txt updated."

install:
	$(ACTIVATE) $(PIP) install -r requirements.txt

migrate:
	$(MANAGE) migrate

create_superuser:
	$(MANAGE) createsuperuser

run:
	$(PYTHON) main.py start

quota: 
	gcloud auth application-default set-quota-project juicy-odds

deploy:
	# Authenticate Docker to Artifact Registry
	gcloud auth configure-docker europe-west1-docker.pkg.dev
	# Build with version
	docker build --build-arg BUILD_VERSION=$(VERSION) -t $(IMAGE_NAME):$(VERSION) .
	# Push only versioned tag
	docker push $(IMAGE_NAME):$(VERSION)
	# Deploy to App Engine
	gcloud app deploy app.yaml --project=juicy-odds --quiet

shell:
	$(ACTIVATE) zsh # Or bash, depending on your preference 

create-repo:
	gcloud artifacts repositories create voice \
    --repository-format=docker \
    --location=europe-west1 \
    --description="Voice agent container images" \
    --project=juicy-odds