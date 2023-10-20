import configparser

import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt

GPT_MODEL = "gpt-3.5-turbo"

import os
conf = configparser.ConfigParser()
conf.read('../config.ini')


os.environ["HTTP_PROXY"] = "http://127.0.0.1:1087"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:1087"

openai.api_key = conf.get("Openai", "api_key")  # 在config.ini中配置自己的APIkey

# openai.api_key = os.getenv("OPENAI_API_KEY")

# 请根据自己的需求调整以下参数
model = 'gpt-3.5-turbo'
max_tokens = 50
temperature = 0.2

# 定义一个名为functions的列表，其中包含两个字典，这两个字典分别定义了两个功能的相关参数
# 第一个字典定义了一个名为"get_current_weather"的function
functions = [
    {
        "name": "get_current_weather",  # function的名称
        "description": "Get the current weather",  # function的描述
        "parameters": {  # 定义该function需要的参数
            "type": "object",
            "properties": {  # 参数的属性
                "location": {  # 地点参数
                    "type": "string",  # 参数类型为字符串
                    "description": "The city and state, e.g. San Francisco, CA",  # 参数的描述
                },
                "format": {  # 温度单位参数
                    "type": "string",  # 参数类型为字符串
                    "enum": ["celsius", "fahrenheit"],  # 参数的取值范围
                    "description": "The temperature unit to use. Infer this from the users location.",  # 参数的描述
                },
            },
            "required": ["location", "format"],  # 该functions需要的必要参数
        },
    },
    # 第二个字典定义了一个名为"get_n_day_weather_forecast"的function
    {
        "name": "get_n_day_weather_forecast",  # function的名称
        "description": "Get an N-day weather forecast",  # function的描述
        "parameters": {  # 定义该function需要的参数
            "type": "object",
            "properties": {  # 参数的属性
                "location": {  # 地点参数
                    "type": "string",  # 参数类型为字符串
                    "description": "The city and state, e.g. San Francisco, CA",  # 参数的描述
                },
                "format": {  # 温度单位参数
                    "type": "string",  # 参数类型为字符串
                    "enum": ["celsius", "fahrenheit"],  # 参数的取值范围
                    "description": "The temperature unit to use. Infer this from the users location.",  # 参数的描述
                },
                "num_days": {  # 预测天数参数
                    "type": "integer",  # 参数类型为整数
                    "description": "The number of days to forecast",  # 参数的描述
                }
            },
            "required": ["location", "format", "num_days"]  # 该function需要的必要参数
        },
    },
]
import json
import requests


class WeatherApi(object):
    """这是一个对接天气预报的api的类
    web url：https://www.apispace.com/
    需要注册登陆该网站并获取apikey，截止：2023-07-28日，该网站每一类接口，新用户有200次免费使用权限
    包括3个方法:，
    1、获取城市代码：get_area_code()
    2、获取当前天气信息：get_current_weather()
    3、获取最近天气信息：get_n_day_weather_forecast()
     """
    headers = {
        "X-APISpace-Token": "",
        "Authorization-Type": "apikey"
    }
    base_url = "https://eolink.o.apispace.com/456456/"

    def get_area_code(self, city, area):
        url = self.base_url + "function/v001/city"

        payload = {"location": city, "items": "1", "area": area, "language": "", "withTz": "", "withPoi": "false"}
        response = requests.request("GET", url, params=payload, headers=self.headers)
        # print(response.text)
        return response.json()["areaList"][0]["areacode"]

    def get_current_weather(self, areacode):
        url = self.base_url + "weather/v001/now"
        payload = {"areacode": areacode}
        response = requests.request("GET", url, params=payload, headers=self.headers)
        # print(response.text)
        return response.text

    def get_n_day_weather_forecast(self, areacode, num_days):
        url = self.base_url + "weather/v001/day"
        payload = {"days": num_days, "areacode": areacode}
        response = requests.request("GET", url, params=payload, headers=self.headers)
        # print(response.text)
        return response.text


def execute_function_call(message):
    """执行函数调用"""
    w_api = WeatherApi()
    if message["function_call"]["name"] == "get_current_weather":
        arguments = json.loads(message["function_call"]["arguments"])
        city, area = str(arguments.get("location")).split(', ')
        areacode = w_api.get_area_code(city, area)
        results = w_api.get_current_weather(areacode)
    elif message["function_call"]["name"] == "get_n_day_weather_forecast":
        arguments = json.loads(message["function_call"]["arguments"])
        city, area = str(arguments.get("location")).split(', ')
        num_days = arguments.get("num_days")
        areacode = w_api.get_area_code(city, area)
        results = w_api.get_n_day_weather_forecast(areacode, num_days)
    else:
        results = f"Error: function {message['function_call']['name']} does not exist"
    return results  # 返回结果


# 1.定义一个函数chat_completion_api，通过 OpenAI Python 库调用 Chat Completions API
@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_api(messages, functions=None, function_call=None, model=GPT_MODEL):
    """
    :param messages:
    :param functions:
    :param function_call: "none" is the default when no functions are present. "auto" is the default if functions are present.
    :param model:
    :return:
    """
    try:
        if functions:
            if function_call:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    functions=functions,
                    function_call=function_call
                )
            else:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    functions=functions,
                    # function_call="auto"
                )
        else:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages
            )
        # 解析返回的数据，获取助手的回复消息
        assistant_message = response["choices"][0]["message"]
        return assistant_message
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def start_chat():
    """
    第一次开始会话时：需要给一个role
    后面每次会话时将前面的内容加载到message里（后面可以优化，如何控制那些内容需要加载进去）
    :return:
    """
    messages = []
    start = 0
    while True:
        if not start:
            content = input(
                "这是一个天气助手，你可以问他：北京，今天天气怎么样？，输入q 并回车结束对话。\nuser: ")
            # 使用append方法向messages列表添加一条系统角色的消息
            messages.append({
                "role": "system",  # 消息的角色是"system"
                "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."
            })
            messages.append({"role": "system", "content": content})
        else:
            content = input("user: ")
            messages.append({"role": "user", "content": content})
        if content == 'q':
            break
        print('message:', messages)  # 可以看到每次输入的message
        res = chat_completion_api(messages, functions)
        # print(f"bot：{res['content']}")
        print(f"bot：{res}")
        messages.append(res)
        start += 1


if __name__ == '__main__':
    start_chat()
