#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <OPENAI_API_KEY>"
    exit 1
fi

OPENAI_API_KEY=$1

# Create the .streamlit directory if it doesn't exist
mkdir -p .streamlit

# Create the secrets.toml file with the API key
echo "OPENAI_API_KEY = \"${OPENAI_API_KEY}\"" > .streamlit/secrets.toml

# Check if Poetry is installed, install if not
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing..."
    curl -sSL https://install.python-poetry.org | python3 -
else
    echo "Poetry is already installed."
fi

# Create the virtual environment using Poetry
poetry env use python3
echo "Virtual environment created successfully using Poetry."

# Install dependencies without root
poetry install --no-root


echo "Setup complete! Your .streamlit/secrets.toml file is ready."
