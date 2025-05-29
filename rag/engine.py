from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os
from dotenv import load_dotenv

class RAGEngine:
    def __init__(self):
        load_dotenv()
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        self.qa_chain = None
        
    def load_documents(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        self.vector_store = Chroma.from_documents(texts, self.embeddings)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(),
            chain_type="stuff",
            retriever=self.vector_store.as_retriever()
        )
    
    async def query(self, question: str, user_context: dict) -> str:
        # Add user context to the question
        enhanced_question = f"User context: {user_context}\nQuestion: {question}"
        response = self.qa_chain.run(enhanced_question)
        return response
