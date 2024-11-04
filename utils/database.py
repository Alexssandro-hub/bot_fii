from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


class MongoDBAtlasFunctions:
    def __init__(self,
                 connection_string="mongodb+srv://Cluster96420:IFNUVEN@cluster96420.zz6rxhr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster96420",
                 db_name='cifii_db',
                 collection_name='embeddings_data',
                 search_index_name='vector_index'):
        """
        Classe para executar funcionalidades de comunicação com o banco de dados MongoDB Atlas.

        Args:
            connection_string (str): string de conexão com o cluster.
            db_name (str): nome do banco de dados definido no Atlas.
            collection_name (str): nome da coleção definido no Atlas.
            search_index_name (str): nome do índice de busca definido no Atlas para execução das querys.
        """

        self.connection_string = connection_string
        self.client = MongoClient(connection_string)

        self.DB_NAME = db_name
        self.COLLECTION_NAME = collection_name
        self.ATLAS_VECTOR_SEARCH_INDEX_NAME = search_index_name

        self.MONGODB_COLLECTION = self.client[self.DB_NAME][self.COLLECTION_NAME]

        self.model_embeddings = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-small-en",
            model_kwargs={"device": "cuda"},
            encode_kwargs={"normalize_embeddings": True}
        )

    def store_embeddings(self, chunks):
        """
        Método para armazenar os vetores de chunks na coleção definida do Atlas.

        Args:
             chunks (list): lista de chunks da classe langchain_core.documents.base.Document.
        """
        MongoDBAtlasVectorSearch.from_documents(
            documents=chunks,
            embedding=self.model_embeddings,
            collection=self.MONGODB_COLLECTION,
            index_name=self.ATLAS_VECTOR_SEARCH_INDEX_NAME
        )

    def get_retriever(self):
        """
        Método para computar o retriever para execução de querys de recuperação dos vetores armazenados.

        Returns:
            langchain_core.vectorstores.VectorStoreRetriever: retriever para execução da querys.
        """
        vector_search = MongoDBAtlasVectorSearch.from_connection_string(
            self.connection_string,
            self.DB_NAME + "." + self.COLLECTION_NAME,
            self.model_embeddings,
            index_name=self.ATLAS_VECTOR_SEARCH_INDEX_NAME)

        qa_retriever = vector_search.as_retriever(search_type="similarity", search_kwargs={"k": 25})
        return qa_retriever
