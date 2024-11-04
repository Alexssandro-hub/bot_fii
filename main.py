from pipeline.generation import GenerationPipeline
from pipeline.indexing import IndexingPipeline
from utils.io_aux import chat_terminal


# DESCOMENTE AS LINHAS ABAIXO PARA COMPUTAR E ARMAZENAR MAIS VETORES NO MONGODB ATLAS
# indexing_pipeline = IndexingPipeline()
# indexing_pipeline.execute()

generation_pipeline = GenerationPipeline()

chat_terminal(generation_pipeline)
