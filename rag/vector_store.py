import hashlib
import os
from xml.dom.minidom import Document

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from model.factory import embedding_model_factory
from utils.config_handler import chroma_conf
from utils.file_handler import (PyPDFLoader, TextLoader, get_file_md5_hex,
                                listdir_with_allower_type)
from utils.logger_handler import logger
from utils.path_tool import get_abs_path


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            persist_directory=get_abs_path(chroma_conf["persist_directory"]),
            embedding_function=embedding_model_factory,
        )

        self.splitter = RecursiveCharacterTextSplitter(
                    chunk_size=chroma_conf["chunk_size"],        # 每个文本块的最大长度
                    chunk_overlap=chroma_conf["chunk_overlap"],  # 相邻文本块之间的重叠长度
                    separators=chroma_conf["separator"],         # 切分文本时优先使用的分隔符列表
                    length_function=len                  # 统计文本长度的方法，这里用len()按字符数计算
                )

    def get_retriever(self, top_k=chroma_conf["topk"]):
            """
            获取向量数据库的检索器，方便加入chain中使用
            :param top_k: 检索时返回的topk个结果，默认使用配置文件中的topk值
            :return: 检索器对象
            """
            return self.vector_store.as_retriever(search_kwargs={"k": top_k})

    def load_document(self):

        def check_md5_hex(md5_for_check:str):
            """
            检查传入的md5字符串是否已经被处理过了
            return: True表示已经处理过了，False表示没有处理过
            """
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                # if进入表示文件不存在，没有处理过md5
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w",encoding="utf-8").close() # 创建空文件
                return False
            else:
                for line in open(get_abs_path(chroma_conf["md5_hex_store"]), "r",encoding="utf-8").readlines():
                    line=line.strip() # 处理字符串前后的空格和回车
                    if line==md5_for_check:
                        return True
                return False

        def save_md5(md5_str: str):
            """
            将传入的md5字符串保存到md5.txt文件中
            """
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a",encoding="utf-8") as f:
                f.write(md5_str + "\n")


        def get_file_document(read_path: str):
            if read_path.endswith(".pdf"):
                return PyPDFLoader(read_path).load()
            elif read_path.endswith(".txt"):
                return TextLoader(read_path, encoding="utf-8").load()

            return []
        def get_string_md5(input_string: str,encoding="utf-8") -> str:
            """将传入的字符串转换为md5值"""

            # 将字符串转换为bytes类型
            str_bytes = input_string.encode(encoding)

            # 计算md5值
            md5_obj = hashlib.md5()  # 得到md5对象
            md5_obj.update(str_bytes)  # 更新内容（传入即将要转换的字节数组）
            md5_str = md5_obj.hexdigest()  # 得到md5值的16进制表示

            return md5_str

        allowed_file_path:list[str]=listdir_with_allower_type(get_abs_path(chroma_conf["data_path"]), allowed_types=tuple(chroma_conf["allowed_extensions"]))

        for path in allowed_file_path:
            # 获取文件的md5
            file_md5 = get_file_md5_hex(path)
            if check_md5_hex(file_md5):
                logger.info(f"文件 {path} 已经处理过，跳过。")
                continue

            try:
                document = get_file_document(path)

                if not document:
                    logger.warning(f"文件 {path} 内没有有效文本内容，跳过。")
                    continue

                split_document:list[Document]=self.splitter.split_documents(document)

                if not split_document:
                    logger.warning(f"文件 {path} 切分后没有有效文本内容，跳过。")
                    continue

                self.vector_store.add_documents(split_document)

                save_md5(file_md5)
                logger.info(f"文件 {path} 已成功处理并添加到向量数据库。")
            except Exception as e:
                logger.error(f"处理文件 {path} 时发生错误: {e}",exc_info=True)
                continue


if __name__ == "__main__":
    vector_store_service = VectorStoreService()
    vector_store_service.load_document()

    retriver = vector_store_service.get_retriever(top_k=3)
    res = retriver.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-"*20)
