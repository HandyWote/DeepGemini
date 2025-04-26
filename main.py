from Ai import *


class DeepZhipu:
    def __init__(self, ai1: str, ai2: str, config_name: str):
        self.ai_map = {
            'deepseek': Deepseek,
            'zhipu': Zhipu,
            'ollama': Ollama
        }
        self.message = []
        self.ai1 = self.ai_map[ai1](config_name)
        self.ai2 = self.ai_map[ai2](config_name)

    def combiner(self):
        pass



if __name__ == '__main__':
    pass