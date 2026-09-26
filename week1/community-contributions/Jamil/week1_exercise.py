import os
import sys
import json
from openai import OpenAI
from dotenv import load_dotenv


OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL_LLAMA = "llama3.2"
MODEL_GPT = "openai/gpt-4o"

 
SYSTEM_PROMPT = (
    "You are a patient, precise technical tutor. Given a technical "
    "question, explain the answer clearly and thoroughly. Use short "
    "code examples where they help. Respond in markdown."
)



def build_message(question):
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"role","content":question}
    ]
    
    return messages


def ask_gpt(question):
    
    load_dotenv(override=True)
    api_key=os.getenv("OPENROUTER_API_KEY")
    base_url="https://openrouter.ai/api/v1"
    client=OpenAI(base_url=base_url,api_key=api_key)
    
    response = client.chat.completions.create(
        model=MODEL_GPT,
        messages=build_message(question),
        max_tokens=3000,
        stream=True
    )
    
    full_text =""
    
    for chunk in response:
        delta = chunk.choices[0].delta.content or ""
        full_text += delta
        print(delta,end="",flush=True)
    print()
    
    return full_text