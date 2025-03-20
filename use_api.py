

import requests
from openai import OpenAI

def get_openai(words):
    url = 'https://api.deepseek.com'
    api = 'sk-667b94f57f894440919c7e1f41402d1c'
    model_name = 'deepseek-reasoner'
    client = OpenAI(api_key = api, base_url=url)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": words},
        ],
        stream=False
    )
    reasoning_content = response.choices[0].message.reasoning_content
    content = response.choices[0].message.content
    total_tokens = response.usage.total_tokens
    return reasoning_content, content, total_tokens

def get_ollama(word):
    url = 'https://localhost:11434/chat'


if __name__ == '__main__':
    rea, con, tok = get_openai('你好')
    print(rea, con, tok)