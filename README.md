# 《AI 大模型应用开发实战营》
- 欢迎来到AI大语言模型训练营！这里是课后练习的文档，供学员们进行课后巩固和练习。
- 最近参加了极客时间《AI 大模型应用开发实战营》，我学习了 AI 大模型的应用开发，以下是参加该训练营的课后练习已经相关总结。
- 该项目包涵： 
  - 大型语言模型的理论和开发基础：深入探究像 GPT-4 这样的大型语言模型的内部运作，包括其架构，训练方法，应用等。 
  - 用 LangChain 开发 AIGC 应用：使用 LangChain 开发 AIGC 应用的实践示例和教程，展示了大型语言模型的实际应用。

- 课程项目地址：https://github.com/ShengqinYang/openai-quickstart
- Fork From：https://github.com/DjangoPeng/openai-quickstart

### 本项目结构如下：

```text
AINote
    datas       --数据集，csv等
    note        --课堂笔记
    project     --项目练习code
        python  --项目py文件类型code
        langchain  --langchain相关学习code【包括5大模块, 文档：https://python.langchain.com/docs/get_started/quickstart】
            model_io  --包涵：模型、prompt、格式化输出
            chains    --整合模型与其他组件，包涵各种不同的chain的使用
            memory    --记住之前的对话。两个功能：读取（READ）和写入（WRITE）
            data_connection  --包涵：文本加载器、文档转换器、文本向量模型、向量数据库、检索器
            agents    --访问其他的工具，比如：给chatgpt增加联网的功能，对接google搜索引擎
        openai_api  --使用openai原生api的相关学习code
    resource    --资源类，如图片
    conifg.ini  --配置文件，存放配置参数，并修改相关配置内容，pull request时切勿暴露私人配置内容
   
```
```text
├── README.md
├── config.ini
├── datas
├── note
├── online_config.ini
├── project
│    ├── langchain
│    │    ├── 8.use_langchain.ipynb
│    │    ├── agents
│    │    │    ├── __init__.py
│    │    │    ├── openai_function.ipynb
│    │    │    ├── react.ipynb
│    │    │    └── self_ask_with_search.ipynb
│    │    ├── chains
│    │    │    ├── 8.homework_router_chain.ipynb
│    │    │    ├── __init__.py
│    │    │    ├── router_chain.ipynb
│    │    │    ├── sequential_chain.ipynb
│    │    │    └── transform_chain.ipynb
│    │    ├── data_connection
│    │    │    ├── __init__.py
│    │    │    ├── document_loader.ipynb
│    │    │    ├── document_transformers.ipynb
│    │    │    ├── text_embedding.ipynb
│    │    │    └── vector_stores.ipynb
│    │    ├── memory
│    │    │    ├── __init__.py
│    │    │    └── mermory.ipynb
│    │    └── model_io
│    │        ├── __init__.py
│    │        ├── model.ipynb
│    │        ├── output_parser.ipynb
│    │        └── prompt.ipynb
│    ├── openai_api
│    │    ├── 3.class_embeddings.ipynb
│    │    ├── 4.class_models.ipynb
│    │    ├── 4.class_tiktoken.ipynb
│    │    └── 5.homework_function_call.ipynb
│    └── python
│        ├── example_chat_completion.md
│        └── example_chat_completion.py
│
└── resource

```

### 练习1：openai_api相关原生的API调用


### 练习2：使用openai_api相关原生的API实现OpenaiTranslator项目
- 项目地址：https://github.com/ShengqinYang/openai-quickstart/tree/main/openai-translator
- Fork From：https://github.com/DjangoPeng/openai-quickstart/tree/main/openai-translator


### 练习3：大模型应用开发框架Langchain相关学习


### 练习4：结合Langchain应用开发框架实现OpenaiTranslator项目
- 项目地址：https://github.com/ShengqinYang/openai-quickstart/tree/main/langchain/openai-translator
- Fork From：https://github.com/DjangoPeng/openai-quickstart/tree/main/langchain/openai-translator


### 练习5：私有化模型部署



## 开源许可证
本项目采用 [Apache 许可证](https://www.apache.org/licenses/LICENSE-2.0) 进行授权。

## 联系我们
如果您在练习过程中遇到任何问题或需要帮助，请随时联系我们：
- 邮箱：jean_open_main@163.com

祝您学习愉快！
