
import requests
from openai import OpenAI
import json


class use_api:
    def __init__(self):
        self.config_name = 'config.json'
        self.model_provider = ''
        self.url = ''
        self.api = ''
        self.model_name = ''
        self.system_prompt = ''
        self.message = []

    def load_config(self, config_name, model_provider):
        try:
            with open(config_name, 'r', encoding='utf-8') as f:
                config = json.load(f)
                config = config[model_provider]
                self.url = config['url']
                self.api = config['api']
                self.model_name = config['model_name']
                self.system_prompt = config['system_prompt']
                self.message = [{"role": "system", "content": self.system_prompt}]
            print("成功加载配置文件")
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            print("请确保config.json文件存在且格式正确")
            exit(1)

    def reload(self):
        self.load_config(self.config_name, self.model_provider)

    def get_openai(self, words):
        try:
            self.message.append({"role": "user", "content": words})
            client = OpenAI(api_key = self.api, base_url= self.url)
            print('发送请求')
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
        except Exception:
            print('请求失败')



    def get_ollama(self, words):
        try:
            self.message.append({"role": "user", "content": words})
            data = {
                "model": self.model_name,
                "messages": self.message,
                "stream": False
            }
            print('发送请求')
            r = requests.post(self.url, json=data).json()
            self.message.append(r['message'])
            content = r['message']['content']
            prompt_count = r['prompt_eval_count']
            return '', content, prompt_count
        except Exception:
            print('请求失败')


if __name__ == '__main__':
    test = use_api()
    test.config_name = 'test_config.json'
    test.model_provider = 'deepseek'
    test.reload()
    cont = test.get_openai('1')
    if cont:
        for i in cont:
            print(i)