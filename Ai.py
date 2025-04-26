import json
import re
from abc import ABC

import requests


class BaseAi(ABC):
    def __init__(self, config_name, model_provider):
        self.words = ''
        self.url = ''
        self.api = ''
        self.model_name = ''
        self.message = []
        self.load_config(config_name, model_provider)
        self.header = {
            "Authorization": f"Bearer {self.api}",
            "Content-Type": "application/json"
        }
    
    def load_config(self, config_name : str, model_provider : str) -> None:
        try:
            with open(config_name, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if model_provider not in config:
                    raise KeyError(f'配置段落 {model_provider} 不存在')
                config = config[model_provider]
                required_fields = ['url', 'api', 'model_name', 'system_prompt']
                for field in required_fields:
                    if field not in config:
                        raise KeyError(f'缺少必要字段: {field}')
                self.url = config['url']
                self.api = config['api']
                self.model_name = config['model_name']
                self.message = [{"role": "system", "content": config['system_prompt']}]
            print("成功加载配置文件")
        except FileNotFoundError:
            print(f"配置文件 {config_name} 未找到")
            exit(1)
        except json.JSONDecodeError:
            print(f"配置文件 {config_name} 格式错误")
            exit(1)
        except KeyError as e:
            print(f"配置字段错误: {str(e)}")
            exit(1)
        except Exception as e:
            print(f"未知错误: {str(e)}")
            exit(1)

    def post_ai(self, words : str) -> dict[str: str]:
        self.message.append({"role" : "user", "content" : words})
        data = {
            "model" : self.model_name,
            "messages" : self.message,
            "stream" : False,
            "temperature": 0.7,  # 新增参数
            "max_tokens": 2000 
        }
        print('\n=== 请求调试信息 ===')
        print(f'请求URL: {self.url}')
        print('请求头:', json.dumps(self.header, indent=2, ensure_ascii=False))
        print('请求体:', json.dumps(data, indent=2, ensure_ascii=False))
        try:
            r = requests.post(self.url, json=data, headers=self.header)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f'请求失败: {str(e)}')
            return {'error': str(e)}

class Deepseek(BaseAi):
    def __init__(self, config_name):
        super().__init__(config_name, 'deepseek')

    def post_ai(self, words : str) -> tuple[str, str, str, list] or tuple[None, None, None, list]:
        r = super().post_ai(words)
        try:
            content = r['choices'][-1]['message']['content']
            reasoning_content = r['choices'][-1]['message']['reasoning_content']
            total_tokens = r['usage']['total_tokens']
            self.message.append({"role": "user", "content": content})
            return reasoning_content, content, total_tokens, self.message
        except (KeyError, IndexError, TypeError) as e:
            print(f"解析响应失败: {str(e)}")
            return None, None, None, self.message

class Zhipu(BaseAi):
    def __init__(self, config_name):
        super().__init__(config_name, 'zhipu')

    def post_ai(self, words : str) -> tuple[str, str, str, list] or tuple[None, None, None, list]:
        r = super().post_ai(words)
        try:
            content = r['choices'][-1]['message']['content']
            reasoning_content = re.search(r'<think>(.*?)</think>', content, re.DOTALL).group(1).strip()
            content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
            total_tokens = r['usage']['total_tokens']
            self.message.append({"role": "user", "content": content})
            return reasoning_content, content, total_tokens, self.message
        except (KeyError, IndexError, TypeError, AttributeError) as e:
            print(f"解析响应失败: {str(e)}")
            return None, None, None, self.message

class Ollama(BaseAi):
    def __init__(self, config_name):
        super().__init__(config_name, 'ollama')

    def post_ai(self, words : str) -> tuple[str, str, str, list] or tuple[None, None, None, list]:
        r = super().post_ai(words)
        try:
            content = r['message']['content']
            reasoning_content = None
            total_tokens = r['prompt_eval_count']
            self.message.append({"role": "user", "content": content})
            return reasoning_content, content, total_tokens, self.message
        except (KeyError, IndexError, TypeError) as e:
            print(f"解析响应失败: {str(e)}")
            return None, None, None, self.message


if __name__ == '__main__':
    a = Ollama('test_config.json')
    for i in a.post_ai('你好'):
        print(i)
    # print(a.post_ai('你好'))