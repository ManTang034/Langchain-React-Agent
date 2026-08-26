"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
from xml.dom.minidom import Document

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model_factory
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompt


def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store_service = VectorStoreService()
        self.retriever = self.vector_store_service.get_retriever()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model_factory
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str, top_k: int = 3)->list[Document]:
        return self.retriever.invoke(input=query)

    def rag_summarize(self, query: str, top_k: int = 3) -> str:

        context_docs = self.retriever_docs(query=query, top_k=top_k)

        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"参考资料{counter}:\n{doc.page_content}\n"

        return self.chain.invoke({"input": query, "context": context})

if __name__ == "__main__":
    rag_service = RagSummarizeService()
    print(rag_service.rag_summarize("小户型适合哪些扫地机器人？"))