<h1 align="center" >NUVEN - CIFII (develop)</h1>


<h1 align='center'>📚 Sobre o Repositório</h1>

Neste repositório está contido o código fonte para o protótipo inicial de um bot para responder perguntas sobre Fundos de Investimentos Imobiliários (FIIs). Todo o código foi desenvolvido utilizando python.

<h1 align='center'> 🎲 Pré Requisitos</h1>

Antes de começar, verifique se você atende aos seguintes pré-requisitos:

- Gerenciador de ambientes Conda instalado.
- CUDA Toolkit 11.7 ou superior instalado.
- Gerenciador de pacotes `pip` instalado.
- `ollama` instalado e rodando.
- Navegador `FireFox` instalado.


<h1 align='center'> 💿 Instalação</h1>

Siga as etapas abaixo para configurar o ambiente de desenvolvimento:

1. Clone este repositório para o seu sistema local.

2. Caso não tenha o ollama instalado, siga os [passos do diretório oficial](https://github.com/ollama/ollama?tab=readme-ov-file) para instalá-lo. *Note que você precisa executar o comando abaixo no powershell em modo administrador para rodar o código*:

   ```bash
    ollama run llama3
    ```

3. Crie um ambiente via `conda` com Python 3.10.0:
   
   ```bash
    conda create -n cifii python=3.10.0
    ```
   
4. Instale no ambiente criado as dependências do projeto utilizando o `pip`:

    ```bash
    pip install -r requirements.txt
    ```

5. Instale o [Ghostscript](https://camelot-py.readthedocs.io/en/master/user/install-deps.html) na sua máquina.


<h1 align='center'> 💿 Executando</h1>

Para executar você precisa digitar no seu terminal o seguinte comando:

 ```bash
python main.py
```

Isso vai iniciar o bot e em seguida permitir que você faça perguntas.  
As perguntas são feitas dentro do próprio terminal.   
O bot vai apresentar duas funções `\clean` (para limpar o histórico) e `\quit` (para sair do bot).

*`OBS 1`*: O carregamento inicial do bot pode levar alguns minutos devido ao processamento inicial dos dados.

*`OBS 2`*: O tempo de reposta de uma pergunta pode levar até 70 segundos (isso pode variar de acordo com seu hardware).

<h1 align='center'> 💿 Documentação </h1>

Uma explicação mais abrangente sobre a tecnologia utilizada pode ser encontrada em [clicando aqui](https://github.com/nuven-cifii/cifii-ia/blob/main/about_bot.MD).
