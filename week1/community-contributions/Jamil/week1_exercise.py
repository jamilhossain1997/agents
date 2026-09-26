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
        {"role":"user","content":question}
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
        max_tokens=1000,
        stream=True
    )
    
    full_text =""
    
    for chunk in response:
        delta = chunk.choices[0].delta.content or ""
        full_text += delta
        print(delta,end="",flush=True)
    print()
    
    return full_text




def ask_ollama(question):
     client=OpenAI(base_url=OLLAMA_BASE_URL,api_key="ollama")
     response = client.chat.completions.create(
         model=MODEL_LLAMA,
         messages=build_message(question),
         stream=True
     )
     
     full_text = ""
     for chunk in response:
             delta = chunk.choices[0].delta.content or ""
             full_text += delta
             print(delta,end="",flush=True)
     print()
     return full_text
 
 
 
def explain(question):
    results = {}
    print("\n=== GPT (via OpenRouter) says ===\n")
    try:
        results["gpt"] = ask_gpt(question)
    except Exception as e:
        print(f"[OpenRouter error: {e}]")

    print("\n=== Llama (Ollama, local) says ===\n")
    try:
        results["llama"] = ask_ollama(question)
    except Exception as e:
        print(f"[Ollama error: {e}]")

    return results




def main():
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter your technical question: ").strip()
    if question:
        explain(question)


if __name__ == "__main__":
    main()