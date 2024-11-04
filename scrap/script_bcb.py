from scrap.Scraper import ScraperInterface
from langchain_community.document_loaders.csv_loader import CSVLoader
import pandas as pd
import os
import shutil


class BCBScraper(ScraperInterface):

    def __init__(self, target_path: str):
        """
        Classe do scrapper da BCB

        Args:
            target_path (str): caminho do diretório dos arquivos.

        Attributes:
            code_list: Lista de códigos de informações da API.
            name_list: Lista dos nomes correspondentes com os códigos.
        """
        super().__init__(target_path)
        self.code_list = [432, 12, 4380, 192, 7456, 433, 21340, 25419, 25785]
        self.name_list = ["selic", "cdi", "pib", "incc", "incc-m", "ipca", "ivg-r", "mvg-r", "sbpe"]

    def scrap(self) -> list:
        """
        Método para realizar o scrap dos dados.

        Returns:
            list: lista de documentos da classe langchain_core.documents.base.Document
        """
        self.download_csv()
        self.merge_csv()

        list_documents = self.loader_csv()

        return list_documents

    def loader_csv(self) -> list:
        """
        Método para carregar os dados na classe do LangChain

        Returns:
            list: lista de documentos da classe langchain_core.documents.base.Document
        """
        for arquivo in os.listdir(self.target_path):
            if arquivo.endswith('.csv'):
                if 'merge' in arquivo:
                    var_path = self.target_path + "/" + arquivo
                    break
        
        path_full_csv_bcb = os.path.join(var_path)

        loader = CSVLoader(file_path=path_full_csv_bcb)
        data_bcb = loader.load()

        return data_bcb

    def query_api_bcb(self, codigo: int):
        """
        Método para fazer a requisição com a API do bcb.

        Args:
            codigo (str): código para puxar a informação pública.

        Returns:
            df: DataFrame com as informações históricos do código informado.
        """
        url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json'
        df = pd.read_json(url)
        
        return df
    
    def download_csv(self) -> None:
        """
        Método para baixar os arquivos CSVs da API.

        Returns:
            None
        """
        data_path = os.path.join(self.target_path)

        if not os.path.exists(data_path):
            os.makedirs(data_path)

        for i in range(len(self.code_list)):
            df = self.query_api_bcb(self.code_list[i])
            df.to_csv(f'{self.name_list[i]}.csv', index=False)

            destino_arquivo = os.path.join(data_path, f'{self.name_list[i]}.csv')
            # Verifica se o arquivo de destino existe e remove
            if os.path.exists(destino_arquivo):
                os.remove(destino_arquivo)
            shutil.move(f'{self.name_list[i]}.csv', data_path)

    def merge_csv(self) -> None:
        """
        Método para mergear os arquivos CSVs da API no diretório.

        Returns:
            None
        """
        dfs = []
        for arquivo in os.listdir(self.target_path):
            if arquivo.endswith('.csv'):
                df = pd.read_csv(os.path.join(self.target_path, arquivo))
                df['acao'] = os.path.splitext(arquivo)[0]

                dfs.append(df)

        target_path_merge = os.path.join(self.target_path, 'merge_csv_BCB.csv')
        merge_csv = pd.concat(dfs, ignore_index=True)  # Concatenar todos os CSVs em um único
        merge_csv.to_csv(target_path_merge)
