from scrap.script_b3 import B3Scraper
from scrap.script_bcb import BCBScraper
from scrap.script_cvm import CVMScraper
# from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from utils.database import MongoDBAtlasFunctions
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings


class IndexingPipeline:
    def __init__(self):
        """
        Classe do pipeline para realizar o processo de Indexing.
        """
        self.scrapers = [B3Scraper('data/data_b3'), BCBScraper('data/data_bcb'), CVMScraper('data/data_cvm')]
        self.db = MongoDBAtlasFunctions()

    def load(self):
        """
        Método para carregar os documentos das fontes de dados.

        Returns:
            list: lista de documentos da classe langchain_core.documents.base.Document.
        """
        documents = []
        for scraper in self.scrapers:
            documents.extend(scraper.scrap())
        return documents

    def get_chunks(self, documents):
        """
        Método para computar os chunks dos documentos.

        Args:
            documents (list): lista de documentos da classe langchain_core.documents.base.Document.

        Returns:
            list: lista de chunks da classe langchain_core.documents.base.Document.
        """

        embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")
        text_splitter = SemanticChunker(embed_model)
        chunks = text_splitter.split_documents(documents)
        return chunks

    def embed(self, chunks):
        """
        Método para computar os embeddings dos documentos.

        Args:
            chunks (list): lista de chunks da classe langchain_core.documents.base.Document.
        """
        self.db.store_embeddings(chunks)

    def execute(self):
        """
        Método para executar o pipeline de Indexing.
        """
        documents = self.load()
        chunks = self.get_chunks(documents)
        self.embed(chunks)
