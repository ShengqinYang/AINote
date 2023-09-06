import os

import faiss
import gradio as gr
import openai
from langchain import SerpAPIWrapper, FAISS, InMemoryDocstore
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.tools import Tool, WriteFileTool, ReadFileTool
from langchain_experimental.autonomous_agents import AutoGPT

openai.api_key = os.getenv("OPENAI_API_KEY")


class AutoGPTTool:
    def __init__(self):
        self.search = SerpAPIWrapper()
        self.tools = [
            Tool(
                name="search",
                func=self.search.run,
                description="useful for when you need to answer questions about current events. You should ask targeted questions",
            ),
            WriteFileTool(),
            ReadFileTool(),
        ]

        self.embeddings_model = OpenAIEmbeddings()
        self.embedding_size = 1536
        self.index = faiss.IndexFlatL2(self.embedding_size)
        self.vectorstore = FAISS(
            self.embeddings_model.embed_query,
            self.index,
            InMemoryDocstore({}),
            {},
        )

        self.agent = AutoGPT.from_llm_and_tools(
            ai_name="檀小椒",
            ai_role="Assistant",
            tools=self.tools,
            llm=ChatOpenAI(temperature=0),
            memory=self.vectorstore.as_retriever(),
        )
        self.agent.chain.verbose = True

    def process_question(self, question):
        return self.agent.run([question])

    def setup_gradio_interface(self):
        iface = gr.Interface(
            fn=self.process_question,
            inputs=[gr.Textbox(lines=5, label="问题", placeholder="请输入问题...")],
            outputs=[gr.Textbox(lines=5, label="答案")],
            title="AutoGPT Chat 小助理",
            description="我是你的AutoGPT小助理：檀小椒，让我们开始聊天吧～",
            theme="soft",
            examples=["2023年9月4日北京的天气怎么样？", "2023年大运会举办地在哪？",
                      "Auto-GPT 是什么？把结果写到autogpt.txt文件中"],
            allow_flagging="never"
        )
        return iface


if __name__ == "__main__":
    # 使用示例
    autogpt_tool = AutoGPTTool()
    gradio_interface = autogpt_tool.setup_gradio_interface()
    gradio_interface.launch(share=True, server_name="0.0.0.0")
