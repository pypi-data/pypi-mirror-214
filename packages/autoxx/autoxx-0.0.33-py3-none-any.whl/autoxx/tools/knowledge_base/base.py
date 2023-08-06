import pinecone,re
import os, time
from typing import Optional,List
from langchain.chat_models import ChatOpenAI
from autoxx.config.config import GlobalConfig
from llama_index.embeddings.openai import OpenAIEmbedding
import logging

from llama_index import (LLMPredictor,
                        ServiceContext,
                        StorageContext,
                        VectorStoreIndex)
from llama_index.indices.loading import load_index_from_storage
from llama_index.storage.docstore import MongoDocumentStore
from llama_index.storage.index_store import MongoIndexStore
from llama_index.vector_stores import PineconeVectorStore
from llama_index.readers.schema.base import Document
from llama_index.node_parser import SimpleNodeParser
from llama_index.langchain_helpers.text_splitter import TokenTextSplitter
from llama_index.callbacks.base import CallbackManager
from llama_index.indices.query.query_transform import HyDEQueryTransform
from llama_index.query_engine.transform_query_engine import TransformQueryEngine
from llama_index.indices.response import ResponseMode

class knowleage_bot:

    def __init__(self, corpus:str, namespace:Optional[str] = None, model:str = "gpt-3.5-turbo", embedding_model: str="text-embedding-ada-002"):
        if not is_valid_corpus_name(corpus):
            raise ValueError(f"Invalid corpus name: {corpus}. coprus name must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character")

        self.corpus = corpus
        self.namespace=namespace
        self.model = model
        self.embedding_model = embedding_model
        mongodb_dbname = self.corpus

        mongodb_password = os.getenv("MONGODB_PASSWORD")
        assert mongodb_password is not None, "Please set MONGODB_PASSWORD environment variable"
        mongodb_user = os.getenv("MONGODB_USER") or "raga"
        mongodb_host = os.getenv("MONGODB_HOST") or "cluster0.spj0g.mongodb.net"
        mongodb_url = f"mongodb+srv://{mongodb_user}:{mongodb_password}@{mongodb_host}/?retryWrites=true&w=majority"

        # create mongodb docstore, indexstore
        self.docstore = MongoDocumentStore.from_uri(uri=mongodb_url, db_name=mongodb_dbname, namespace=f"{self.namespace}/doc_store")
        self.index_store = MongoIndexStore.from_uri(uri=mongodb_url, db_name=mongodb_dbname, namespace=f"{self.namespace}/index_store")
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        assert pinecone_api_key is not None, "Please set PINECONE_API_KEY environment variable"
        pinecone_environment =  os.getenv("PINECONE_ENVIRONMENT") or "us-central1-gcp"

        pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
        index_list = pinecone.list_indexes()
        if self.corpus not in index_list:
            print(f"vector index {self.corpus} not found, creating...")
            pinecone.create_index(name=self.corpus, metric="cosine", dimension=1536)
        pinecone_index = pinecone.Index(self.corpus)
        self.vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace=self.namespace)

        storage_context = StorageContext.from_defaults(
            docstore=self.docstore,
            index_store=self.index_store,
            vector_store=self.vector_store,
        )

        config = GlobalConfig().get()
        llm_model_config = config.get_llm_model_config(self.model)
        llm = ChatOpenAI(model_name= llm_model_config.model, model_kwargs={
            "api_key": llm_model_config.api_key,
            "api_base": llm_model_config.api_base,
            "api_type": llm_model_config.api_type,
            "api_version": llm_model_config.api_version,
            "deployment_id": llm_model_config.api_deployment_id
        })
        llm_predictor_chatgpt = LLMPredictor(
            llm=llm
        )
        embed_model_config = config.get_embedding_model_config(self.embedding_model)
        embed_model = OpenAIEmbedding(
            deployment_name=embed_model_config.api_deployment_id,
            api_key=embed_model_config.api_key,
            api_base=embed_model_config.api_base,
            api_type=embed_model_config.api_type,
            api_version=embed_model_config.api_version,
        )
       
        service_context = ServiceContext.from_defaults(
            llm_predictor=llm_predictor_chatgpt, chunk_size_limit=2048, embed_model=embed_model,
            node_parser=SimpleNodeParser(
                text_splitter=TokenTextSplitter(
                    callback_manager=CallbackManager([]),
                    chunk_size = 2048,
            ))
        )

        try:
            self.index = load_index_from_storage(
                storage_context=storage_context, service_context=service_context
            )
        except ValueError as e:
            if "No index in storage context" in str(e):
                # create a new index
                self.index = VectorStoreIndex(
                    nodes = [],
                    storage_context=storage_context,
                    service_context=service_context,
                )
            else:
               raise e

    def query(self, query:str, enable_hype:bool = True, retrieve_top_k:int = 3):
        start_time = time.time()
        query_engine = self.index.as_query_engine(similarity_top_k=retrieve_top_k)

        if enable_hype:
            hyde = HyDEQueryTransform(include_original=True)
            query_engine = TransformQueryEngine(query_engine, hyde)

        try:
            response = query_engine.query(query)
            logging.info(f"query: {query}, response: {response}, cost: {time.time() - start_time}")
            return response
        except Exception as e:
            print("Error:", e)
            raise Exception(f"failed to finish query: {str(e)}")

    def similarity_search(self, query:str, enable_hype:bool = True, retrieve_top_k:int = 3):
        start_time = time.time()
        query_engine = self.index.as_query_engine(similarity_top_k=retrieve_top_k)
        if enable_hype:
            hyde = HyDEQueryTransform(include_original=True)
            query_engine = TransformQueryEngine(query_engine, hyde)

        try:
            response =  query_engine.retrieve(query)
            logging.info(f"query: {query}, response: {response}, cost: {time.time() - start_time}")
            return response
        except Exception as e:
            print("Error:", e)
            raise Exception(f"failed to retrieve nodes: {str(e)}")

    def upsert_document(self, documents: List[Document]) -> None:
        self.index.docstore.add_documents(documents, allow_update=True)
        for document in documents:
            nodes = self.index.service_context.node_parser.get_nodes_from_documents([document])
            print(nodes)
            self.index.insert_nodes(nodes)

    def delete_document(self, document_id: str) -> None:
        self.index.delete_ref_doc(document_id)
        self.index.docstore.delete_document(document_id)
        try:
            self.vector_store.delete(document_id, namespace=self.namespace)
        except Exception as e:
            print(f"failed to delete vector for document {document_id}: {str(e)}")

    def retrieve_document(self, document_ids: List[str]) ->  List[Document]:
        if document_ids is None or len(document_ids) == 0:
            return [doc for _, doc in self.index.docstore.docs.items()]

        documents = []
        for document_id in document_ids:
            document = self.index.docstore.get_document(document_id)
            documents.append(document)
        return documents

def is_valid_corpus_name(corpus_name):
    # Regular expression pattern for the corpus name rule
    pattern = r'^[a-z0-9][a-z0-9-]*[a-z0-9]$'

    # Check if the corpus name matches the pattern
    if re.match(pattern, corpus_name):
        return True
    else:
        return False