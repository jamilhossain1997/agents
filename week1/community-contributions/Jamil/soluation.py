from openai import OpenAI
from scraper import fetch_website_contents

OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL = "llama3.2"

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""


def message_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website},
    ]


def summarize(url):
    client = OpenAI(api_key="ollama", base_url=OLLAMA_BASE_URL)
    website = fetch_website_contents(url)

    response = client.chat.completions.create(
        model=MODEL,
        messages=message_for(website),
    )
    return response.choices[0].message.content


def main():
    url = input("Enter the URL to summarize: ")
    print("\nFetching and summarizing...\n")
    summary = summarize(url)
    print(summary)


if __name__ == "__main__":
    main()