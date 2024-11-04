from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_llm():
    """
    Função para retornar o modelo LLM para geração de texto.

    Returns:
        langchain_community.llms.ollama.Ollama: modelo LLM.
    """
    llm = Ollama(model="llama3")
    return llm


def get_prompt(prompt_history):
    """
    Função para computar o template do prompt de entrada para o LLM.

    Args:
        prompt_history (bool): booleano que indica se o prompt retornado deve ser o referente ao histórico.

    Returns:
        langchain_core.prompts.chat.ChatPromptTemplate: template do prompt de entrada.
    """
    if prompt_history:
        prompt = """
        Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is.
        """
    else:
        prompt = """
        You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer, just say that you don't know. \
        Use three sentences maximum and keep the answer concise.\
        {context}
        """
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    return qa_prompt
