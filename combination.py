from use_api import *

if __name__ == '__main__':
    deepseek = use_api()
    deepseek.config_name = 'test_config.json'
    deepseek.model_provider = 'deepseek'
    deepseek.reload()

    ollama = use_api()
    ollama.config_name = 'test_config.json'
    ollama.model_provider = 'ollama'
    ollama.system_prompt = '你是一个助手请根据我给出的推理过程，整理出结果'
    ollama.reload()

    quesetion = ('用中文写一篇搞笑小故事')
    d_r, d_a, d_t = map(str, deepseek.get_openai(quesetion))
    o_r, o_a, o_t = map(str, ollama.get_ollama(d_r+'所以'+quesetion))

    print(d_a+'\n'+d_t)
    print(o_a+'\n'+o_t)