import os
import sys
import json
from openai import OpenAI


OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL = "llama3.2"

 
SYSTEM_PROMPT = (
    "You are a patient, precise technical tutor. Given a technical "
    "question, explain the answer clearly and thoroughly. Use short "
    "code examples where they help. Respond in markdown."
)