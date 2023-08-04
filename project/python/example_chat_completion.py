import configparser
import openai
import os

conf = configparser.ConfigParser()
conf.read('../config.ini')
openai.api_key = conf.get("Openai", "api_key")  # 在config.ini中配置自己的APIkey
os.environ["HTTP_PROXY"] = conf.get("Proxy", "HTTP_PROXY")  # 配置自己的代理
os.environ["HTTPS_PROXY"] = conf.get("Proxy", "HTTPS_PROXY")

# 请根据自己的需求调整以下参数
model = 'gpt-3.5-turbo'
max_tokens = 500
temperature = 0.2


def chat_with_bot(message):
    """
    :param message: eg: {"role": "system", "content": "you are a translation assistant"})
    :return: eg: {"role": "assistant", "content": "...."})
    """
    # ChatCompletion
    conversation_3 = openai.ChatCompletion.create(
        model=model,
        messages=message,
        # max_tokens=max_tokens,
        temperature=temperature,
    )
    answer = conversation_3['choices'][0]["message"]
    new_message_dict = {"role": answer.role, "content": answer.content}
    return new_message_dict


def start_chat():
    """
    第一次开始会话时：需要给一个role
    后面每次会话时将前面的内容加载到message里（后面可以优化，如何控制那些内容需要加载进去）
    :return:
    """
    message = []
    start = 0
    while True:
        if not start:
            content = input(
                "首次开始会话，请定义角色以及简单描述：如：你是我的翻译助手，请帮我将下面的内容翻译成中文，输入q 并回车结束对话。\nprompt system: ")
            message.append({"role": "system", "content": content})
            userinput = input("user：")
            message.append({"role": "user", "content": userinput})
        else:
            content = input("user： ")
            message.append({"role": "user", "content": content})
        if content == 'q':
            break
        # print('message:', message)  # 可以看到每次输入的message
        res = chat_with_bot(message)
        print(f"{res['role']}：{res['content']}")
        message.append(res)
        start += 1


if __name__ == '__main__':
    start_chat()

# 你是专业的著作翻译家，帮我翻译成中文，确保翻译后的句子流畅连贯，并与原文意思保持一致。内容：The quick brown fox jumps over the lazy dog. This pangram contains every letter of the English alphabet at least once. Pangrams are often used to test fonts, keyboards, and other text-related tools. In addition to English, there are pangrams in many other languages. Some pangrams are more difficult to construct due to the unique characteristics of the language.
