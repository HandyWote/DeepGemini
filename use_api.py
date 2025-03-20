

import requests
from openai import OpenAI
class use_api:
    def __init__(self):
        self.message = [{"role": "system", "content": "You are a helpful assistant"}]
        self.url = 'https://api.deepseek.com'
        self.api = ''
        self.model_name = 'deepseek-reasoner'

    def get_openai(self, words):
        self.message.append({"role": "user", "content": words})
        client = OpenAI(api_key = self.api, base_url= self.url)
        response = client.chat.completions.create(
            model=self.model_name,
            messages=self.message,
            stream=False
        )
        self.message.append(response.choices[0].message)
        reasoning_content = response.choices[0].message.reasoning_content
        content = response.choices[0].message.content
        total_tokens = response.usage.total_tokens
        return reasoning_content, content, total_tokens

    def get_ollama(self, words):
        url = 'http://127.0.0.1:11434/api/chat'
        model_name = 'llama3.2:latest'
        system_prompt = ''
        beforecontent = ''
        data = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": words
                }],
            "stream": False
        }
        r = requests.post(url, json=data).json()
        self.message.append(r['message'])
        content = r['message']['content']
        prompt_count = r['prompt_eval_count']
        return content, prompt_count

if __name__ == '__main__':
    api = use_api()
    rea, c = api.get_ollama('你好')
    print(rea,'\n',c)