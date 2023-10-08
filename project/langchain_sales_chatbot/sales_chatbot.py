import os

import gradio as gr
import configparser
from langchain import (FAISS, SerpAPIWrapper, OpenAI, PromptTemplate, LLMChain)
from langchain.agents import initialize_agent, AgentType
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.output_parsers import RegexParser
from langchain.tools import Tool

from utils.logger import LOG
from utils.argument_parser import ArgumentParser
from utils.sales_confg import SalesConfig

conf = configparser.ConfigParser()
current_directory = os.path.dirname(os.path.realpath('__file__'))
config_file_path = os.path.join(current_directory, '..', '..', 'config.ini')
conf.read(config_file_path)

if not os.getenv("OPENAI_API_KEY"):
    os.environ['OPENAI_API_KEY'] = conf.get("Openai", "api_key")  # 在config.ini中配置自己的APIkey

if not os.getenv("SERPAPI_API_KEY"):
    os.environ['SERPAPI_API_KEY'] = conf.get("SerpApi", "serp_apikey")  # 在config.ini中配置自己的serp_apikey


class SalesChatbot(object):
    chat_model = "gpt-3.5-turbo"
    text_model = "text-davinci-003"

    def __init__(self):
        self.llm = ChatOpenAI(model_name=self.chat_model, temperature=0)
        self.db = FAISS.load_local(folder_path=config.db_name, embeddings=OpenAIEmbeddings())

    def initialize_sales_bot(self):
        """使用 Faiss 作为向量数据库，去向量数据里做内容检索"""
        global SALES_BOT
        retriever = self.db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.8, 'k': 1}  # 按相关性去查找, k默认返回几条
        )
        SALES_BOT = RetrievalQA.from_chain_type(self.llm, retriever=retriever)
        # 返回向量数据库的检索结果
        SALES_BOT.return_source_documents = True
        return SALES_BOT

    def add_qa(self, q: str, a: str):
        """加到向量数据库"""
        qa = f"[客户问题] {q}\n[销售回答] {a}"
        self.db.add_texts([qa])
        self.db.save_local(folder_path=config.db_name)
        LOG.info(f"加到向量数据库：问题：{q}，结果：{a}")

    def use_search_api(self, query: str):
        """
        use SerpAPI
        """
        prompt = " 用中文回答我。"
        query += prompt
        print(query)
        search = SerpAPIWrapper()
        tools = [Tool(name="Intermediate Answer",
                      func=search.run,
                      description="当你需要通过搜索来询问时很有用"),
                 ]
        agent = initialize_agent(
            tools, self.llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True
        )
        res = agent.run(query)
        LOG.info(f"使用搜索引擎：问题：{query}，结果：{res}")
        return res

    def check_topic_relevance(self, q: str, a: str):
        """检查话题相关性"""
        role_prompt = config.role_prompt
        check_template = PromptTemplate.from_template(
            f"{role_prompt}"
            "下面是一段Q&A问答对：\n"
            "问题：{question}\n"
            "答案：{answer}\n"
            "判断Q&A问答对是否与你的角色强相关，如果是，则回答：是，否则回答：不是"
        )
        print(check_template)
        output_parser = RegexParser(regex="([\u4e00-\u9fa5]+)", output_keys=['keys'])
        checkLLMChain = LLMChain(llm=self.llm, prompt=check_template, output_parser=output_parser)
        result = checkLLMChain.run({"question": q, "answer": a})
        LOG.info(f"检查话题相关性：问题：{q}，结果：{a}")
        return result

    def check_sure_answer(self, q: str, a: str):
        """
        q:问题
        a:答案
        """
        check_template = PromptTemplate.from_template(
            "这是一段Q&A问答对：\n"
            "问题：{question}\n"
            "答案：{answer}\n"
            "判断答案是否是不确定的，如果是不确定，则回答：'不确定'，否则回答：'确定'。"
        )
        output_parser = RegexParser(regex="([\u4e00-\u9fa5]+)", output_keys=['keys'])
        checkLLMChain = LLMChain(llm=self.llm, prompt=check_template, output_parser=output_parser)
        result = checkLLMChain.run({"question": q, "answer": a})
        LOG.info(f"检查Q&A确定性：确定性：{result['keys']}｜问题：{q}｜答案：{a}")
        return result

    def sales_boot(self, message: str, history: list):
        # print(f"[message]{message}")
        print(f"[history]{history}{type(history)}")
        # TODO 加一个功能，判断问题是否在历史记录里，如果在则从历史记录里提取
        # TODO 加一个功能，维护有用的相关的历史历史记录
        ans = SALES_BOT({"query": message})
        # 如果检索出结果，或者开了大模型聊天模式，返回 RetrievalQA combine_documents_chain 整合的结果
        if ans["source_documents"] or config.enable_chat:
            result = ans['result']
            LOG.info(f"向量数据库搜索结果：{result}")
            check_answer = self.check_sure_answer(message, result)  # 功能：检查RetrievalQA检索结果｜大语言模型的回答 是否满足问题
            if check_answer.get("keys") == "不确定":
                search_api_answer = self.use_search_api(message)  # 功能：答案不确定时，使用搜索引擎
                # TODO 搜索结果的正确的待验证
                relevance_answer = self.check_topic_relevance(message, search_api_answer)  # 功能：搜索结果如果跟本小助手有高相关性 则将Q&A加到向量数据库里
                if relevance_answer.get("keys") == "是":
                    self.add_qa(message, search_api_answer)
                return search_api_answer
            else:
                return ans["result"]
        # 否则输出套路话术
        else:
            LOG.info("不使用大模型聊天模式～")
            return f"作为一个{config.title}，我暂时不知道这个问题的答案，但是我会继续努力学习的～"

    def launch_gradio(self, config: SalesConfig):
        demo = gr.ChatInterface(
            fn=self.sales_boot,
            title=config.title,
            description=config.description,
            examples=config.examples,
            # retry_btn=None,
            # undo_btn=None,
            chatbot=gr.Chatbot(height=600),
        )

        demo.launch(share=True, server_name="0.0.0.0")


if __name__ == "__main__":
    # 解析命令行
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 初始化配置单例
    config = SalesConfig()
    config.initialize(args)

    sales_bot = SalesChatbot()
    sales_bot.initialize_sales_bot()

    sales_bot.launch_gradio(config)
    # print(sales_bot.search_api("2023年iphone发布会时间是什么时候？"))
    # print(sales_bot.check_topic_relevance("2023年iphone发布会时间是什么时候？", "2023年iPhone将于9月13日发布。"))
