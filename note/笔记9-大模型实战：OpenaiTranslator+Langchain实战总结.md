## 学习笔记：结合 OpenAI-Translator 与 Langchain 大模型开发框架，优化OpenAI-Translator项目
- 项目地址：https://github.com/ShengqinYang/openai-quickstart/tree/main/langchain/openai-translator
- Fork From：https://github.com/DjangoPeng/openai-quickstart/tree/main/langchain/openai-translator

- OpenAI-Translator项目，新旧结构对比：

<div style="display: flex; justify-content: center;">
<div style="flex-grow: 1;">


```plaintext 
V-1.0 结构：
openai-translator
├── ai_translator
│   ├── __init__.py
│   ├── book
│   │   ├── book.py
│   │   ├── content.py
│   │   └── page.py
│   ├── main.py
│   ├── model
│   │   ├── glm_model.py
│   │   ├── model.py
│   │   └── openai_model.py
│   ├── translator
│   │   ├── pdf_parser.py
│   │   ├── pdf_translator.py
│   │   ├── exceptions.py
│   │   └── writer.py
│   └── utils
│       ├── argument_parser.py
│       ├── config_loader.py
│       └── logger.py
├── config.yaml
├── fonts
├── images
├── jupyter
├── requirements.txt
└── tests
```  
 </div>

<div style="flex-grow: 1;">

```plaintext
V-2.0 结构：
openai-translator
├── ai_translator
│    ├── __init__.py
│    ├── book
│    │   ├── book.py
│    │   ├── content.py
│    │   └── page.py
│    ├── flask_server.py
│    ├── gradio_server.py
│    ├── main.py
│    ├── translator
│    │    ├── __init__.py
│    │    ├── exceptions.py
│    │    ├── pdf_parser.py
│    │    ├── pdf_translator.py
│    │    ├── translation_chain.py
│    │    ├── translation_config.py
│    │    └── writer.py
│    └── utils
│        ├── __init__.py
│        ├── argument_parser.py
│        └── logger.py
├── config.yaml
├── fonts
├── images
├── requirements.txt
└── tests
```

</div>
</div>

## 整体对比：
### 第一、模型调用优化
* V-1.0：使用各个模型自己的原生的api，举例：使用openai的模型，需要自定义封装调用ChatCompletion和Completion API，构造prompt、构造请求等
* V-2.0：使用Langchain封装的统一的模型接口，用一个LLMChain，传入相应的模型名称即可，使用统一的Prompt，以及构造请求。具体code：translation_chain.py
  ```python
   chat = ChatOpenAI(model_name=model_name, temperature=0, verbose=verbose)  
   chain = LLMChain(llm=chat, prompt=chat_prompt_template, verbose=verbose)
  ```

<div style="display: flex; justify-content: center;">
<div style="flex-grow: 1;">

```plaintext 
V-1.0 痛点：

1. 重复的大模型扩展工作
2. LLM相关方法和接口不统一，维护成本高                
3. Prompt 与 Model 耦合                            ————>
4. 子类需手动区分 LLM 和 Chat Model
         
         
                                  
│   ├── model
│   │   ├── glm_model.py
│   │   ├── model.py                              ————>
│   │   └── openai_model.py



```  
 </div>

<div style="flex-grow: 1;">

```plaintext
V-2.0 优化：

1. 使用 LangChain 框架替代自己造轮子
2. Model I/O 覆盖主流大模型，提供标准接口 
3. 使用 Chains 管理 Prompt 与 Model
4. 框架原生支持 LLM 和 Chat Model 两类模型


│    ├── translator
│    │    ├── __init__.py
│    │    ├── exceptions.py
│    │    ├── pdf_parser.py
│    │    ├── pdf_translator.py
│    │    ├── translation_chain.py
│    │    ├── translation_config.py
│    │    └── writer.py
```
</div>

</div>


### 第二、项目参数配置优化
- V-1.0，项目启动配置比较复杂没有很好的封装
- V-2.0，使用单例模式进行全局配置管理，封装了TranslationConfig类，具体code：translation_config.py
- 调用对比
<div style="display: flex; justify-content: center;">
<div style="flex-grow: 0;">

```python
V-1.0：

argument_parser = ArgumentParser()
args = argument_parser.parse_arguments()
config_loader = ConfigLoader(args.config)

config = config_loader.load_config()

model_name = args.openai_model
if args.openai_model else config['OpenAIModel']['model']
api_key = args.openai_api_key if args.openai_api_key \
    else config['OpenAIModel']['api_key']
model = OpenAIModel(model=model_name, api_key=api_key)

pdf_file_path = args.book if args.book else config['common']['book']
file_format = args.file_format if args.file_format \
    else config['common']['file_format']

# 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
translator = PDFTranslator(model)
translator.translate_pdf(pdf_file_path, file_format)
```
 </div>

<div style="flex-grow: 1;">


```python
V-2.0：

# 解析命令行
argument_parser = ArgumentParser()
args = argument_parser.parse_arguments()

# 初始化配置单例
config = TranslationConfig()
config.initialize(args)    

# 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
translator = PDFTranslator(config.model_name)
translator.translate_pdf(config.input_file, 
                         config.output_file_format, 
                         pages=None)






```
</div>

</div>


### 第三、新增基于 Gradio 的图形化界面设计

### 第四、新增基于 Flask 的Web服务化API


