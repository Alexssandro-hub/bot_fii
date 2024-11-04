<h1 align="center" >Coleta e Organização dos Dados</h1>

<h1 align='center'>📚 Sobre a Documentação</h1>
Esta documentação descreve todo o processo de coleta e organização dos dados, também destacando as bases de dados escolhidas e motivações.

Destaca-se que essa etapa está em sua versão inicial. Futuramente, as bases de dados serão revisadas para avaliar possíveis melhorias que possam ser aplicadas na extração. Além disso, o código será refatorado e comentado para melhor entendimento e legibilidade.

<h1 align='center'> 🎲 Bases de Dados</h1>

Essa seção destaca as 3 bases de dados escolhidas para o projeto: BCB, CVM e B3. Nas próximas subseções, são realizados comentários acerca de cada uma das bases, apontando quais de suas estruturas foram extraídas e as motivações.

<h2 align='center'> Banco Central do Brasil (BCB) </h2>
O BCB fornece os dados do mercado com vários indicadores da conjuntura econômica tais como: taxa de juros, taxa de câmbio, endividamento do setor público, aplicações financeiras, inadimplência etc. Por meio dos dados da BACEN, o chatbot pode obter informações de fatores macroeconômicos que possuem a capacidade de influenciar diversos tipos de FIIs.

Atualmente, os seguintes indicadores são extraídos dessa base:

- Certificado de Depósito Interbancário (CDI)
- Índice Nacional de Custo de Construção (INCC)
- Índice Nacional de Custo de Construção — Mercado (INCC-M)
- Índice Nacional de Preços ao Consumidor Amplo (IPCA)
- Índice de Valores de Garantia de Imóveis Residenciais Financiados (IVG-R)
- Mediana dos Valores de Garantia de Imóveis Residenciais Financiados (MVG-R)
- Produto Interno Bruto (PIB)
- Sistema Brasileiro de Poupança e Empréstimo (SBPE)
- Sistema Especial de Liquidação e Custódia (SELIC)

<h2 align='center'> Comissão de Valores Mobiliários (CVM)</h2>
A Comissão de Valores Mobiliários (CVM) é a reguladora do mercado de capitais no Brasil. Possui dados dos diversos FIIs cadastrados, bem como informações relevantes do mercado imobiliário. A CVM armazena diversos documentos que servem de comunicação entre a gestão de um FII e seus investidores, transmitindo informações relevantes para o investimento.

Atualmente, as seguintes categorias de documentos são extraídas dessa base:

- Fato Relevante
- Atos de Deliberação do Administrador
- Oferta Pública de Aquisição de Cotas
- Laudo de Avaliação (conclusão de Negócio)
- Aviso aos Cotistas - Estruturado
- Regulamento de Emissores B3
- Assembleia
- Listagem e Admissão à Negociação de Cotas
- Comunicado ao Mercado
- Aviso aos Cotistas
- Outras Demonstrações Financeiras
- Regulamento
- Informes Periódicos
- Relatórios
- Oferta Pública de Distribuição de Cotas
- Políticas de Governança Corporativa
- Outras Informações

<h2 align='center'> B3 </h2>
A B3 é a bolsa de valores do Brasil. Nela concentram-se todas as transações do mercado de capitais do Brasil. Possui informações diárias das cotações dos FIIs além de outros dados relevantes. As informações extraídas da B3 focam, principalmente, em capturar o comportamento dos investidores e dos investimentos da bolsa de valores.

Atualmente, os dados extraídos dessa base são os do Boletim Mensal dos Fundos Imobiliários. As seguintes informações são extraídas:

- Top 10 FIIs mais negociados no último mês e último ano
- Top 10 FIIs mais rentáveis no último mês e último ano
- Composição da cateria teórica IFIX

<h1 align='center'> ⚙️ Pipeline de Processamento</h1>

Este projeto aplica a arquitetura Retrieval Augmented Generation (RAG) utilizando a biblioteca LangChain, destacada na figura abaixo:

![rag_image](../figs/rag_pipeline.png?raw=True)

Pela figura, podemos ver dois principais componentes na arquitetura RAG: um conjunto de documentos e um modelo generativo LLM. Dado uma pergunta do usuário, são recuperados seções dos documentos que possuem similaridade com o contexto da pergunta. O prompt de entrada para o LLM é composto tanto pela pergunta como por esse conjunto de documentos.

A grande vantagem dessa arquitetura é a falta de necessidade de retreinamento da LLM, pois os conhecimentos específicos sobre os FIIs são vindos externamentes pelos documentos armazenados. Além disso, o conhecimento do modelo é atualizado apenas com uma atualização no conjunto de documentos, garantindo um maior desempenho em fornecer respostas atualizadas com fatos recentes, característica importantíssima em investimentos. 

Assim, este projeto possui duas principais funcionalidades: 

- a atualização do banco de documentos;
- a aplicação do modelo generativo LLM.

A segunda funcionalidade é bem direta: o LLM vai responder às perguntas de usuários utilizando o banco de documentos como fonte de conhecimento externo.

A atualização do banco de documentos é uma funcionalidade realizada periodicamente. Caso necessário, ela pode ser ativada forçadamente por algum usuário administrador. Essa funcionalidade está apresentada na figura abaixo: 

![indexing_image](../figs/indexing_pipeline.png?raw=True)

Primeiramente, os documentos são extraídos das bases de dados escolhidas (BCB, CVM e B3). Então, esses documentos são divididos em seções (chunks). Para otimizar o algoritmo de busca dos chunks no banco de dados, eles são armazenados como vetores (embeddings). A etapa de atualização do banco é finalizada. 

Atualmente, o scrapping e o armazenamento dos embeddings das bases de dados é realizado com sobrescrita. Futuramente vai ser implementada uma funcionalidade para apenas adicionar novas informações com as já existentes.
