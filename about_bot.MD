<h1 align='center'> 💿 Tecnologia utilizadas </h1>

Nosso bot é baseado no conceito Retrieval Augmented Generation (RAG). O `RAG` permite você inserir novos conhecimentos na LLM sem precisar retreiná-la. Para isso você, a estratégia é ter a sua disposição uma base de dados textual contendo os novos conhecimentos que sua LLM vai precisar. O truque é você buscar via similaridade os trechos de texto, na sua base de dados, que são mais parecidos com sua entrada da LLM. Esses trechos de texto + entrada da LLM + prompt de comando irão alimentar a LLM final, o que por fim permite ela responder perguntar cujas respostas não estão previstas em seu conhecimento prévio. Em outras palavras, o RAG apenas insere a resposta da sua pergunta para a LLM já na própria entrada, e o que a LLM faz nada mais é que filtrar, sintetizar e terminar de elaborar a resposta final. As imagens abaixo ilustram todo esse passo a passo do funcionamento do RAG.

![passo de tratamento dos dados](./figs/indexing_pipeline.png)
Na figura acima, podemos ver como a base de dados textual é preparada para ser concumida pelo RAG. Inicialmente são carregados arquivos com os conteúdos, esses arquivos são quebrados em chuncks para reduzir a quantidade de tokens de entrada das LLMs e também reduzir ruído ou alucinações. Os chuncks são codificados em vetores utilizando algum tipo de encoder. E por fim esses vetores são armazenados.

![passo de tratamento dos dados](./figs/rag_pipeline.png)
Na figura acima já temos o fluxo desde a pergunta inicial ao bot, passando pela etapa de busca de chuncks mais similares a pergunta inicial, depois concatenando o resultado da busca e a pergunta de entrada ao prompt de comando, e por fim alimentando a LLM com esse texto e adquirindo a resposta.

<h1 align='center'> 💿 Algumas considerações </h1>

Dentro dos passos que compõem o RAG existe muito espaço para otimização. Cada etapa possui uma infinidade de possibilidades de construção visando uma recuperação mais rápida e correta dos chuncks, além de rotinas de filtragem e desvios de fluxo para realizar novas buscas de novos chuncks. Ou seja, a implementação de um RAG é algo bem complexo e requer muita pesquisa para entender qual a melhor estratégia e quais os melhores componentes para se utilizar.  


Atualmente nosso RAG conta com muitos recursos de ponta que vão desde a etapa inicial de coleta, chunckenização, codificação e armazenamento dos dados, passando pela escrita do prompt de entrada (engenharia de prompt), passando pela função que reescreve a query inicial do usuário para deixar ela mais entendível, depois passando pela etapa de busca dos chunks, passando por funções que verificam a qualidade dos chuncks encontrados e uma possível nova busca, até escolha da LLM mais adequada para responder, e por fim por funções que verificam a qualidade da resposta baseada na query inicial dando espaço para uma geração de outra resposta mais coerente.

- Todo o nosso bot foi construindo utilizando o framework langchain escrito em python. 
- A LLM utilizado foi o llama3:8b.  
- Nós utilizamos o chunck semântico.
- Adotamos a estratégia de parental retriever.
- Os dados foram armazenados no atlas server.
- Os dados foram coletadas de 3 fontes de dados distintas (B3, BCB e CVM) via webscrap.

Existia a possibilidade de integração de conceitos de GraphRAG ao pipeline. Esse conceito daria mais flexibilidade ao RAG e permitiria buscas na web, desvios de fluxo mais otimizados e inteligentes, menor perda de conhecimento pela etapa do retriever, e mais verificações de alunação.

<h1 align='center'> 💿 Links úteis </h1>

- [langchain](https://python.langchain.com/v0.1/docs/get_started/introduction)
- [rag angchain](https://python.langchain.com/v0.2/docs/tutorials/rag/)
- [langgraph](https://www.langchain.com/langgraph)
- [ollama](https://github.com/ollama/ollama)
- [GraphRAG](https://blog.langchain.dev/agentic-rag-with-langgraph/)
- [Tipos de RAG](https://medium.com/@drjulija/what-are-naive-rag-advanced-rag-modular-rag-paradigms-edff410c202e)