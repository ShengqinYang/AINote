## 进阶篇：学习笔记：结合 OpenAI-Translator 与 Langchain 大模型开发框架，优化OpenAI-Translator项目
### 第一部分：OpenAI-Translator V-1.0 与 V-2.0总结
- 项目地址：https://github.com/ShengqinYang/openai-quickstart/tree/main/langchain/openai-translator
- Fork From：https://github.com/DjangoPeng/openai-quickstart/tree/main/langchain/openai-translator

- OpenAI-Translator项目，新旧结构对比：

<div style="display: flex; justify-content: center;">
<div style="flex-grow: 0;">


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

<div style="flex-grow: 0;">

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

### 整体对比：
#### 第一、模型调用优化
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


#### 第二、项目参数配置优化
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


#### 第三、新增基于 Gradio 的图形化界面设计；新增基于 Flask 的Web服务化API

- V-1.0 版本仅支持main.py启动项目
- V-2.0 版本：
  ```text
  1、支持本地启动项目，启动文件 main.py
  2、支持 Gradio 的图形化界面，启动文件 gradio_server.py
  3、基于 Flask 的Web服务化API，启动文件 flask_server.py
  ```

```python
 # 2、支持 Gradio 的图形化界面
def launch_gradio():
        
    iface = gr.Interface(
        fn=translation,
        title="OpenAI-Translator v2.0(PDF 电子书翻译工具)",
        inputs=[
            gr.File(label="上传PDF文件"),
            gr.Textbox(label="源语言（默认：英文）", placeholder="English", value="English"),
            gr.Textbox(label="目标语言（默认：中文）", placeholder="Chinese", value="Chinese")
        ],
        outputs=[
            gr.File(label="下载翻译文件")
        ],
        allow_flagging="never"
    )

    # iface.launch(share=True, server_name="0.0.0.0")
    iface.launch()
```

```python
# 3、基于 Flask 的Web服务化API
@app.route('/translation', methods=['POST'])
def translation():
    try:
        input_file = request.files['input_file']
        source_language = request.form.get('source_language', 'English')
        target_language = request.form.get('target_language', 'Chinese')

        LOG.debug(f"[input_file]\n{input_file}")
        LOG.debug(f"[input_file.filename]\n{input_file.filename}")

        if input_file and input_file.filename:
            # # 创建临时文件
            input_file_path = TEMP_FILE_DIR+input_file.filename
            LOG.debug(f"[input_file_path]\n{input_file_path}")

            input_file.save(input_file_path)

            # 调用翻译函数
            output_file_path = Translator.translate_pdf(
                input_file=input_file_path,
                source_language=source_language,
                target_language=target_language)
            
            # 移除临时文件
            # os.remove(input_file_path)

            # 构造完整的文件路径
            output_file_path = os.getcwd() + "/" + output_file_path
            LOG.debug(output_file_path)

            # 返回翻译后的文件
            return send_file(output_file_path, as_attachment=True)
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response), 400
```


### 第二部分：课后习题
  - 1.在 openai-translator gradio 图形化界面基础上，支持风格化翻译，如：小说、新闻稿、作家风格等。
  - 2.添加一些按钮，按钮对应function，预置风格化的翻译，如：小说、新闻稿、特定作家风格(鲁迅)等
  - 3.基于 ChatGLM2-6B 实现图形化界面 的 openai-translator
  - 新功能：
    - 1.支持多语言；
    - 2.支持多输出文件格式， 新增word格式输出；
    - 3.支持多翻译风格；
    - 4.新增下拉框选项
  - [项目代码](../project/langchain_openai_translator/ai_translator/gradio_server.py)
  - [项目启动说明](../project/langchain_openai_translator/README.md)
  - [展示](../resource/homework_openai_translator_v2.0.png)


  

