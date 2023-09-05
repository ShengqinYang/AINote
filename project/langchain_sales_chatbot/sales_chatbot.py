import os

import gradio as gr
import openai
from langchain import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

from utils.argument_parser import ArgumentParser
from utils.sales_confg import SalesConfig

chat_model = "gpt-3.5-turbo"
openai.api_key = os.getenv("OPENAI_API_KEY")


def initialize_sales_bot(config):
    """使用 Faiss 作为向量数据库，去向量数据里做内容检索"""
    # print(db_name, type(db_name), "db_name")
    db = FAISS.load_local(config.db_name, OpenAIEmbeddings())
    llm = ChatOpenAI(model_name=chat_model, temperature=0)
    global SALES_BOT
    SALES_BOT = RetrievalQA.from_chain_type(llm,
                                            retriever=db.as_retriever(
                                                search_type="similarity_score_threshold",
                                                search_kwargs={"score_threshold": 0.8, 'k': 1}  # 按相关性去查找, k默认返回几条
                                            ))
    # 返回向量数据库的检索结果
    SALES_BOT.return_source_documents = True

    return SALES_BOT


def sales_boot(message, history):
    print(f"[message]{message}")
    print(f"[history]{history}")
    ans = SALES_BOT({"query": message})
    # 如果检索出结果，或者开了大模型聊天模式
    # 返回 RetrievalQA combine_documents_chain 整合的结果
    if ans["source_documents"] or config.enable_chat:
        print(f"[result]{ans['result']}")
        print(f"[source_documents]{ans['source_documents']}")
        return ans["result"]
    # 否则输出套路话术
    else:
        return f"作为一个{config.title}，我暂时不知道这个问题的答案，但是我会继续努力学习的～"


def launch_gradio(config):
    demo = gr.ChatInterface(
        fn=sales_boot,
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
    initialize_sales_bot(config)

    launch_gradio(config)
