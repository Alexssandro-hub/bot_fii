from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_core.messages import HumanMessage
from utils.model import get_llm, get_prompt
from utils.database import MongoDBAtlasFunctions


class GenerationPipeline:
    def __init__(self):
        """
        Classe do pipeline para realizar a geração de texto via Retrieval Augmented Generation (RAG).
        """
        self.db = MongoDBAtlasFunctions()
        self.__make_rag_chain()
        self.chat_history = []

    def __make_rag_chain(self):
        """
        Método privado para construir o pipeline do RAG que será utilizado.
        """
        retriever = self.db.get_retriever()

        contextualize_q_prompt = get_prompt(prompt_history=True)
        qa_prompt = get_prompt(prompt_history=False)

        llm = get_llm()
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

        self.rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    def answer(self, question: str):
        """
        Método para responder uma pergunta de entrada utilizando o pipeline do RAG.

        Args:
            question (str): string contendo uma pergunta.

        Returns:
            str: string contendo a resposta.
        """
        rag_result = self.rag_chain.invoke({'input': question, 'chat_history': self.chat_history})
        self.chat_history.extend([HumanMessage(content=question), rag_result['answer']])
        return rag_result['answer']
