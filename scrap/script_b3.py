import os
import re
import time
import camelot
import requests
import pandas as pd
import pypdfium2 as pdfium
from scrap.Scraper import ScraperInterface
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.document_loaders.csv_loader import CSVLoader
from selenium import webdriver as wd
from selenium.webdriver.common.by import By


class B3Scraper(ScraperInterface):

    def __init__(self, target_path: str):
        """
         Classe do scrapper da B3

        Args:
            target_path (str): caminho do diretório dos arquivos.
        """
        super().__init__(target_path)

    def documents(self):
        """
        Método para que executa as funções getData() e data() que são, respectivamente, referente ao scrapping dos dados através do site da b3, o processamento e o salvamento em csv.
        
        Returns:
            langchain_community.document_loaders.directory.DirectoryLoader: documentos.
        """
        
        self.get_data()
        self.data()
        docs = DirectoryLoader(
                path=self.target_path,
                glob=f"**/*{'.csv'}",
                loader_cls=CSVLoader,
                show_progress=True
            )
        
        return docs

    def scrap(self) -> list:
        """
        Método "Main" que retorna a lista com todos os documentos (csv) carregados que foram pegos através do scrapping.
        
        Returns:
            list: lista dos documentos carregados da classe langchain_core.documents.base.Document
        """
        docs = self.documents()
        docs_load = docs.load() 

        return docs_load

    def get_data(self) -> str:
        """
        Método para acessar o site da B3 e baixar o PDF do boletim mensal, onde estão os dados.

        Returns:
            str: path para os arquivos salvos.
        """

        # Cria o diretório especificado, caso não exista
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)

        navigator = wd.Firefox()
        url = "https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/fundos-de-investimento-imobiliario-fii.htm"
        navigator.get(url)
        time.sleep(1)
        url_download = navigator.find_element(By.XPATH, '/html/body/main/div[4]/div/div[2]/div[1]/div[2]/nav/ul/li[3]/a').get_attribute('href')
        filename = url_download.split("/")[-1]
        response = requests.get(url_download)
        directory = os.path.join(self.target_path, filename)

        with open(directory, 'wb') as f:
            f.write(response.content)
        
        navigator.quit()

        return directory
    
    def data(self):
        """
        Método geral para processar e chamar o método que salva os dados.
        """

        for root, dirs, files in os.walk(self.target_path):
            for file in files:
                filepath = os.path.join(root, file)
                if file.endswith(".pdf"):
                    print(f"ARQUIVO: {file}")
                    pdf = pdfium.PdfDocument(filepath)
                    loader = PyPDFLoader(filepath)
                    pages = loader.load_and_split()
                    num_pages = len(pages)
                    for i in range(num_pages):
                        dados = []
                        current_page = self.organyze_text(pages[i].page_content)
                        #Using camelot
                        if "FIIs MAIS RENTÁVEIS" in current_page: 
                            fiis_perfomance = self.performance_fiis(filepath, i)
                        elif "FIIs MAIS NEGOCIADOS" in current_page:
                            most_traded_fiis = self.most_traded_fiis(filepath, dados, i)
                        #Using pdfium
                        elif "CARTEIRA TEÓRICA IFIX" in current_page:
                            categorical_portfolio = self.ifix_categorical(pdf[i])
                        
                    self.csv(most_traded_fiis, fiis_perfomance, categorical_portfolio, file.split(".")[0])

    def organyze_text(self, text_all):
        """
        Método usado para organizar o conteúdo.

        Args:
            text_all: retorno da função get_text_range() da biblioteca 

        Returns:
            list: o conteúdo da página organizado em uma lista.
        """
        sentences = []
        words = ''
        for char in text_all:
            if char == '\n' or char == '\r':
                if words:
                    sentences.append(words)
                    words = ''
            else:
                words += char
        return sentences
    
    def most_traded_fiis(self, filepath: str, dados: list, page_index: int):
        """
        Método usado para organizar o conteúdo da página referente aos FIIs mais negociados.

        Args:
            filepath (str): caminho do arquivo.
            dados (list): variável temporária.
            page_index (int): número da página .

        Returns:
            list: número de dataframes de acordo com a quantidade de tabelas que tem na página,
                geralmente são 2.
        """
        all_dfs = []
        table = camelot.read_pdf(filepath, pages=str(page_index+1))
        qtd_tables = len(table)

        for i in range(qtd_tables):
            df = table[i].df
            df_columns = df.iloc[0]
            df = df[1:]
            columns = []
            for column in df_columns:
                columns.append(column.split('\n'))
            columns = sum(columns, [])
            if len(columns) == 4:
                for _, data in df.iterrows():
                    data[0] = data[0].split('\n')
                    data[1] = data[1].split('\n')
                    if len(data[0]) > 2:
                        code = ''.join(data[0][:2])
                        name = ''.join(data[0][2:])
                        data[0] = [code, name]
                    sum_elements = sum([data[0], data[1]], [])
                    dados.append(sum_elements)
                    
                new_df = pd.DataFrame(columns=columns)       
                for index, dado in enumerate(dados):
                    if len(dado) == len(columns):
                        new_df.loc[index] = dado
                    else:
                        print(f"Os dados {dado} não têm a mesma quantidade de columns que o DataFrame.")

                new_df['Newsletter date'] = 'April/2024'
                all_dfs.append(new_df)

        return all_dfs
    
    def performance_fiis(self, filepath: str, page_index: int, ):
        """
        Método usado para organizar o conteúdo da página referente aos FIIs mais rentáveis.

        Args:
            filepath (str): caminho do arquivo.
            page_index (int): número da página.

        Returns:
            list: número de dataframes de acordo com a quantidade de tabelas que tem na página,
                geralmente são 2.
        """
        all_dfs = []
        table = camelot.read_pdf(filepath, pages=str(page_index+1))
        qtd_tables = len(table)

        for i in range(qtd_tables):
            df = table[i].df
            dados = []
            if i == 1:
                df_columns = ['Codigo', 'Nome', 'Variação mensal do preço de fechamento']
            else:
                df_columns = ['Codigo', 'Nome', 'Variação anual do preço de fechamento']
            for _, data in df.iterrows():
                data[0] = data[0].split('\n')
                code = None
                nome = ""
                for dado in data[0]:
                    padrao = r'\b[A-Z]{4}\d{2}\b'
                    nome_temp = re.sub(padrao, '', dado).strip()
                    if dado[:4].isupper() and dado[4:6].isdigit():
                        code = dado
                        index_code = data[0].index(code)
                        if len(code) < 6:
                            code = data[0][index_code-1] + code
                
                    nome += " " + nome_temp    

                data[0] = [code, nome.strip()]
                sum_elements = sum([data[0], [data[1]]], [])
                dados.append(sum_elements)
            new_df = pd.DataFrame(columns=df_columns)       
            for j, dado in enumerate(dados):
                if len(dado) == len(df_columns):
                    new_df.loc[j] = dado
                else:
                    print(f"Os dados {dado} não têm a mesma quantidade de colunas que o DataFrame.")

            new_df['Newsletter date'] = 'April/2024'
            all_dfs.append(new_df)
        
        return all_dfs

    def ifix_categorical(self, page):
        """
        Método usado para organizar o conteúdo da página referente a carteira IFIX.

        Args:
            page: Atual página do PDF.

        Returns:
            list: um dataframe com todas as informações acerca da carteira IFIX.
        """
        data = {}
        new_data = {}
        dfs = []
        tabela_atual = 1
        text_all = page.get_textpage().get_text_range()
        sentences_page = self.organyze_text(text_all)

        df = pd.DataFrame(columns=["Ação", "Código", "Part.(%)", "Qtde.Teórica"])

        data[tabela_atual] = []
        for line in sentences_page:
            if 'Ação' in line or 'Part' in line or 'Qtde' in line or "Teórica" in line:
                tabela_atual += 1  # Incrementa o número da tabela
                data[tabela_atual] = []  # Inicializa a lista de dados para a próxima tabela
            else:
                # Se não for um cabeçalho de tabela, adiciona a linha aos dados da tabela atual
                data[tabela_atual].append(line)
        data.pop(1)
        data = {key: value for key, value in data.items() if value}

        for key, values in data.items():
            empty_value = ""
            acao = []
            codigo = []
            part = []
            test = []
            for value in values:
                if '%' not in value:
                    acao_codigo = value.split()
                    acao.append(acao_codigo[0])
                    codigo.append(acao_codigo[1])
                else:
                    part_test = value.split()
                    part.append(part_test[0])
                    test.append(part_test[1])
            if len(acao) < len(part): 
                acao.append(empty_value)
                codigo.append(empty_value)
            elif len(acao) > len(part): 
                part.append(empty_value)
                test.append(empty_value)

            new_data[key] = {'Ação': acao, 'Código': codigo, 'Part.(%)': part, 'Qtde.Teórica': test}
        for chave, valores in new_data.items():
            #print(f'A quantidade de dados pegados por tabela é \n {chave}:{len(valores["Ação"]), len(valores["Código"]), len(valores["Part.(%)"]), len(valores["Qtde.Teórica"])}')
            df_temp = pd.DataFrame({
                "Ação": valores["Ação"],
                "Código": valores["Código"],
                "Part.(%)": valores["Part.(%)"],
                "Qtde.Teórica": valores["Qtde.Teórica"]
            })
            dfs.append(df_temp)
        df = pd.concat(dfs, ignore_index=True)
        df.insert(len(df.columns),'Newsletter date' ,'April/2024')

        return df
    
    def csv(self, most_traded_fiis, fiis_perfomance, categorical_portfolio, filename):
        filename7 = f'{filename}_most_traded_fiis_month.csv'
        filename7_2 = f'{filename}_most_traded_fiis_year.csv'
        filename8 = f'{filename}_fiis_perfomance_year.csv'
        filename8_2 = f'{filename}_fiis_perfomance_month.csv'
        filename9 = f'{filename}_categorical_portfolio.csv'
        with open(os.path.join(self.target_path, filename7), 'w', encoding='utf-8') as f:
            most_traded_fiis[1].to_csv(f, index=False)
        with open(os.path.join(self.target_path, filename7_2), 'w', encoding='utf-8') as f:
            most_traded_fiis[0].to_csv(f, index=False)
        with open(os.path.join(self.target_path, filename8), 'w', encoding='utf-8') as f:
            fiis_perfomance[1].to_csv(f, index=False)
        with open(os.path.join(self.target_path, filename8_2), 'w', encoding='utf-8') as f:
            fiis_perfomance[0].to_csv(f, index=False)
        with open(os.path.join(self.target_path, filename9), 'w', encoding='utf-8') as f:
            categorical_portfolio.to_csv(f, index=False)
