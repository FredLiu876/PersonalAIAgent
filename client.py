import toml

from openai import OpenAI

with open(".streamlit/secrets.toml", "r") as f:
    data = toml.load(f)

GPT_MODEL = "gpt-4-turbo"

client = OpenAI(
    api_key=data["OPENAI_API_KEY"]
)
