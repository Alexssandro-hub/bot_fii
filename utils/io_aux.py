def chat_terminal(generation_pipeline):
    """
    Função para interagir com o pipeline de geração de texto com RAG via terminal.

    Args:
        generation_pipeline (GenerationPipeline): pipeline de geração de texto.
    """
    print('para sair digite /bye')

    while True:
        question = input("Faça uma pergunta: ")
        if question == '/bye':
            break
        else:
            print(generation_pipeline.answer(question))
