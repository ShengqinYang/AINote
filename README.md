# 《AI 大模型应用开发实战营》

- 欢迎来到AI大语言模型训练营！这里是课后练习的文档，供学员们进行课后巩固和练习。
- 最近参加了极客时间《AI 大模型应用开发实战营》，我学习了 AI 大模型的应用开发，以下是参加该训练营的课后练习已经相关总结。
- 该项目包涵：
    - 大型语言模型的理论和开发基础：深入探究像 GPT-4 这样的大型语言模型的内部运作，包括其架构，训练方法，应用等。
    - 用 LangChain 开发 AIGC 应用：使用 LangChain 开发 AIGC 应用的实践示例和教程，展示了大型语言模型的实际应用。

- 课程项目地址：https://github.com/ShengqinYang/openai-quickstart
- Fork From：https://github.com/DjangoPeng/openai-quickstart

### 练习1：[openai_api相关原生的API调用](./project/openai_api)

### 练习2：使用openai_api相关原生的API实现OpenaiTranslator项目

- 项目地址：https://github.com/ShengqinYang/openai-quickstart/tree/main/openai-translator
- Fork From：https://github.com/DjangoPeng/openai-quickstart/tree/main/openai-translator

### 练习3：大模型应用开发框架Langchain相关学习

- [LangChain](./note/笔记8-大模型应用开发框架-LangChain.md)
    - LangChain 是什么
    - 为什么需要 LangChain
    - LangChain 典型使⽤场景
    - LangChain 基础概念与模块化设计
- [LangChain 5大核⼼模块⼊⻔与实战](./project/langchain)
    - Model I/O： -- 包涵：Models、Prompt、Output Parsers
    - chains --整合模型与其他组件，包涵各种不同的chain的使用
    - memory --记住之前的对话。两个功能：读取（READ）和写入（WRITE）
    - data_connection --包涵：文本加载器、文档转换器、文本向量模型、向量数据库、检索器
    - agents --访问其他的工具，比如：给chatgpt增加联网的功能，对接google搜索引擎
- [LangChain 5大核⼼模块源码结构梳理](./resource/AI-LangChain.xmind)

### 练习4：[结合Langchain应用开发框架实现OpenaiTranslator项目](./note/笔记9-大模型实战：OpenaiTranslator+Langchain实战总结.md)

- [实战 LangChain 版 OpenaiTranslator项目](./project/langchain_openai_translator)

### 练习5：[网红项目 AutoGPT 深度学习](./note/笔记10-大模型实战：基于Langchain实现AutoGpt功能.md)

- AutoGPT 原始版本定位与功能解读
- LangChain 版 AutoGPT 技术方案与架构设计
    - 网络搜索（SerpAPIWrapper）模块
    - 文件读写（FileTool）模块
    - 持久化存储（VectorStores）模块
    - 向量模型（Embeddings）模块
    - 聊天模型（Chat Models）模块
- [实战 LangChain 版 AutoGPT](./project/langchain_autogpt)

### 练习6：[基于知识库的销售顾问 Sales-Consultant](./note/笔记11-大模型实战：基于知识库的房产销售Sales-Consultant.md)

- Sales-Consultant 市场需求分析
- Sales-Consultant 产品定义与功能规划
- Sales-Consultant 技术方案与架构设计
    - 解析与索引管理（Indexes）模块
    - 知识库问答（QA Chain）模块
    - 用户引导（Example Selectors）模块
- [实战 LangChain 版 Sales-Consultant](./project/langchain_sales_chatbot)

### 练习7：[基于ChatGLM2-6B-int4私有化模型部署](./project/langchain/model_io/model_chatglm.ipynb)

## 开源许可证

本项目采用 [Apache 许可证](https://www.apache.org/licenses/LICENSE-2.0) 进行授权。

## 联系我们

如果您在练习过程中遇到任何问题或需要帮助，请随时联系我们：

- 邮箱：jean_open_main@163.com

祝您学习愉快！
