import requests
from openai import OpenAI
import json


class use_api:
    def __init__(self):
         self.load_config()


    def load_config(self):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)

                ollama_config = config['ollama']
                self.ollama_url = ollama_config['url']
                self.ollama_api = ollama_config['api']
                self.ollama_model_name = ollama_config['model_name']
                system_prompt = ollama_config['system_prompt']
                self.ollama_message = [{"role": "system", "content": system_prompt}]

                openai_config = config['openai']
                self.openai_url = openai_config['url']
                self.openai_api = openai_config['api']
                self.openai_model_name = openai_config['model_name']
                system_prompt = openai_config['system_prompt']
                self.openai_message = [{"role": "system", "content": system_prompt}]

            print("成功加载配置文件")
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            print("请确保config.json文件存在且格式正确")
            exit(1)


    def get_openai(self, words):
        self.openai_message.append({"role": "user", "content": words})
        client = OpenAI(api_key = self.openai_api, base_url= self.openai_url)
        response = client.chat.completions.create(
            model=self.openai_model_name,
            messages=self.openai_message,
            stream=False
        )
        self.openai_message.append(response.choices[0].message)
        reasoning_content = response.choices[0].message.reasoning_content
        content = response.choices[0].message.content
        total_tokens = response.usage.total_tokens
        return reasoning_content, content, total_tokens


    def get_ollama(self, words):
        self.ollama_message.append({"role": "user", "content": words})
        data = {
            "model": self.ollama_model_name,
            "messages": self.ollama_message,
            "stream": False
        }
        r = requests.post(self.ollama_url, json=data).json()
        self.ollama_message.append(r['message'])
        content = r['message']['content']
        prompt_count = r['prompt_eval_count']
        return content, prompt_count


if __name__ == '__main__':
    test = use_api()
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

        ollama_config = config['ollama']
        test.ollama_url = ollama_config['url']
        test.ollama_api = ollama_config['api']
        test.ollama_model_name = ollama_config['model_name']
        system_prompt = ollama_config['system_prompt']
        test.ollama_message = [{"role": "system", "content": system_prompt}]

        openai_config = config['openai']
        test.openai_url = openai_config['url']
        test.openai_api = openai_config['api']
        test.openai_model_name = openai_config['model_name']
        system_prompt = openai_config['system_prompt']
        test.openai_message = [{"role": "system", "content": system_prompt}]
    cont = test.get_ollama('你好')
    print(cont)