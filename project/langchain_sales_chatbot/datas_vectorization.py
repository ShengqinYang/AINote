import openai
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
import configparser, os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    conf = configparser.ConfigParser()
    current_directory = os.path.dirname(os.path.realpath('__file__'))
    config_file_path = os.path.join(current_directory, '..', '..', 'config.ini')
    conf.read(config_file_path)
    api_key = conf.get("Openai", "api_key")  # 在config.ini中配置自己的APIkey
    os.environ['OPENAI_API_KEY'] = api_key

chat_model = "gpt-3.5-turbo"


def read_file(file_name):
    """读取文本"""
    with open(file_name) as f:
        file_datas = f.read()
    return file_datas


def split_datas(file_datas, split_str=r'\n\n---\n\n'):
    """文本拆分"""
    text_splitter = CharacterTextSplitter(
        separator=split_str,
        chunk_size=150,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=True,
    )
    docs = text_splitter.create_documents([file_datas])
    print(docs[1])
    return docs


def datas_to_embeddings(docs, db_name):
    """使用 Faiss 作为向量数据库，持久化存储房产销售 问答对（QA-Pair）"""
    try:
        db = FAISS.from_documents(docs, OpenAIEmbeddings())

        if not os.path.exists(db_name):  # 向量数据库文件不存在就创建并保存
            db.save_local(db_name)
        else:
            old_db = FAISS.load_local(db_name, OpenAIEmbeddings())  # 向量数据库文件存在就添加并保存
            old_db.merge_from(db)
            old_db.save_local(db_name)
        return True
    except Exception as e:
        raise e


def query_db(db_name, query):
    """使用 Faiss 作为向量数据库，去向量数据里做内容检索"""
    db = FAISS.load_local(db_name, OpenAIEmbeddings())
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.8, 'k': 1, "fetch_k": 2}  # 按相关性去查找, k默认返回几条

    )
    docs = retriever.get_relevant_documents(query)
    if docs:
        for d in docs:
            return d.page_content.split("：**")[-1]
    else:
        return "没有符合条件的回答"


def main(file_name, db_name, split_str):
    """
    主函数：读取文本、分割文本、向量化、存到向量数据库
    """
    file_datas = read_file(file_name)
    docs = split_datas(file_datas, split_str)
    res = datas_to_embeddings(docs, db_name)
    return res


if __name__ == "__main__":
    # 房地产销售问答数据
    # file_name = "files/real_estate_sales_data_1.txt"
    # db_name = "real_estate_sales"
    # split_str = r'\n\n---\n\n'

    # 苹果销售问答数据
    file_name = "files/apple_Q&A_datas_3.txt"
    db_name = "apple_Q&A_datas_embedding"
    split_str = r'\d+\.'

    # query = "iphone最新型号有哪些？"
    # query = "北京今天天气怎么样？"
    # query = "2023年iphone什么时候发布？"
    query = "2023年iPhone都发布什么型号？"
    # query = "北京朝阳区的苹果实体店有哪些？"
    # query = "四川省的省会是哪里？"
    # query = "周边的交通如何？"
    # result = main(file_name, db_name, split_str) # 读取文本、分割文本、向量化、存到向量数据库
    # db = FAISS.load_local(db_name, OpenAIEmbeddings())
    # q = "2023年iphone什么时候发布"
    # a = "2023年iPhone将于9月13日发布。"
    # qa = f"[客户问题] {q}\n[销售回答] {a}"
    # db.add_texts([qa])
    # db.save_local(folder_path=db_name)
    result = query_db(db_name, query)  # 从向量数据库检索

    print(result)
