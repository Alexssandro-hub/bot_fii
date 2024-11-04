class ScraperInterface:
    def __init__(self, target_path: str):
        """
        Interface que determina o comportamento de um scraper de uma determinada fonte de dados.

        Args:
            target_path (str): caminho do diretório dos arquivos.
        """
        self.target_path = target_path

    def scrap(self) -> list:
        """
        Método para realizar o scrap dos dados.

        Returns:
            list: lista de documentos da classe langchain_core.documents.base.Document
        """
        pass
