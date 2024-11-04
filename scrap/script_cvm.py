from scrap.Scraper import ScraperInterface
import os
import time
import shutil
import datetime as DT
from selenium import webdriver
from selenium.webdriver.common.by import By
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.xml import UnstructuredXMLLoader


class CVMScraper(ScraperInterface):

    def __init__(self, target_path: str):
        """
        Classe do scrapper da CVM

        Args:
        target_path (str): caminho do diretório dos arquivos.
        """
        super().__init__(target_path)
        self.temp_path = os.path.join(os.getcwd(), 'temp_cvm')
        self._create_folders()
        self.driver = self._init_webdriver()
        
    def _init_webdriver(self):
        """
        Método que inicia, configura e cria o driver firefox para acessar e baixar os dados da CVM.
        """
        
        options = webdriver.FirefoxOptions()
        
        # confidurando driver do firefox
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", self.temp_path)
        options.set_preference("browser.download.directory_upgrade", True)
        options.set_preference("browser.download.prompt_for_download", False)
        options.set_preference("browser.download.manager.alertOnEXEOpen", False)
        options.set_preference("browser.download.manager.focusWhenStarting", False)
        options.set_preference("browser.helperApps.alwaysAsk.force", False)
        options.set_preference("browser.download.manager.closeWhenDone", True)
        options.set_preference("browser.download.manager.showAlertOnComplete", False)
        options.set_preference("browser.download.manager.useWindow", False)
        
        options.set_preference("pdfjs.disabled", True)
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.set_preference("network.proxy.socks_remote_dns", True)
        
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        
        return driver
    
    def _create_folders(self):
        """
        Método que verifica se os diretórios para armazenar temporáriamente os documentos da CVM
        existem. Se não existirem, então o método irá criá-los.
        """

        folders_names = [self.temp_path,
                        self.target_path,
                        os.path.join(self.target_path, 'Fato Relevante'),
                        os.path.join(self.target_path, 'Outras Informações'),
                        os.path.join(self.target_path, 'Atos de Deliberação do Administrador'),
                        os.path.join(self.target_path, 'Oferta Pública de Aquisição de Cotas'),
                        os.path.join(self.target_path, 'Laudo de Avaliação (conclusão de Negócio)'),
                        os.path.join(self.target_path, 'Aviso aos Cotistas - Estruturado'),
                        os.path.join(self.target_path, 'Regulamento de Emissores B3'),
                        os.path.join(self.target_path, 'Assembleia'),
                        os.path.join(self.target_path, 'Listagem e Admissão à Negociação de Cotas'),
                        os.path.join(self.target_path, 'Comunicado ao Mercado'),
                        os.path.join(self.target_path, 'Aviso aos Cotistas'),
                        os.path.join(self.target_path, 'Outras Demonstrações Financeiras'),
                        os.path.join(self.target_path, 'Regulamento'),
                        os.path.join(self.target_path, 'Informes Periódicos'),
                        os.path.join(self.target_path, 'Relatórios'),
                        os.path.join(self.target_path, 'Oferta Pública de Distribuição de Cotas'),
                        os.path.join(self.target_path, 'Políticas de Governança Corporativa')]

        # Pasta onde os PDFs serão salvos
        for output_folder in folders_names:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
        
    def _download_datas(self):
        """
        Método que realiza o download dos dados da cvm.
        """

        link = "https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM"
        
        self.driver.get(link)
        
        month = self.driver.find_element(By.XPATH, value='/html/body/form/div/div/div/button')
        month.click()
        time.sleep(5)

        # escolhendo tipo de fundo como fundo imobiliário
        month = self.driver.find_element(By.XPATH, value='/html/body/div[3]/div/form/div/div[1]/div/div')
        month.click()
        time.sleep(5)
        month = self.driver.find_element(By.XPATH, value='/html/body/div[6]/ul/li[7]/div')
        month.click()
        time.sleep(5)

        # setando o status para ativo
        month = self.driver.find_element(By.XPATH, value='/html/body/div[3]/div/form/div/div[6]/div/div')
        month.click()
        time.sleep(5)
        month = self.driver.find_element(By.XPATH, value='/html/body/div[7]/ul/li[2]/div')
        month.click()
        time.sleep(5)

        today = DT.date.today()
        week_ago = today - DT.timedelta(days=1)
        week_ago = week_ago.strftime('%d/%m/%Y')

        month = self.driver.find_element(By.XPATH, value="/html/body/div[3]/div/form/div/div[8]/div/input[@name='dataInicial']")
        month.click()
        time.sleep(5)
        month.send_keys(week_ago)

        # aplicando filtros
        month = self.driver.find_element(By.XPATH, value='/html/body/div[3]/div/form/div/div[12]/div/input')
        month.click()
        time.sleep(5)

        all_categorys = ['Categoria', 'Fato Relevante', 'Outras Informações', 'Atos de Deliberação do Administrador',
                        'Oferta Pública de Aquisição de Cotas', 'Laudo de Avaliação (conclusão de Negócio)',
                        'Aviso aos Cotistas - Estruturado', 'Regulamento de Emissores B3', 'Assembleia',
                        'Listagem e Admissão à Negociação de Cotas', 'Comunicado ao Mercado', 'Aviso aos Cotistas',
                        'Outras Demonstrações Financeiras', 'Regulamento', 'Informes Periódicos', 'Relatórios',
                        'Oferta Pública de Distribuição de Cotas', 'Políticas de Governança Corporativa']

        for category in range(2, 19, 1):
            # abrindo aba de filtros
            month = self.driver.find_element(By.XPATH, value='/html/body/form/div/div/div/button')
            month.click()
            time.sleep(5)
            month = self.driver.find_element(By.XPATH, value='/html/body/div[3]/div/form/div/div[3]/div/div')
            month.click()
            time.sleep(5)
            month = self.driver.find_element(By.XPATH,
                                        value='/html/body/div[8]/ul/li[' + str(category) + ']/div')  # li de 2 até 18
            month.click()
            time.sleep(5)
            # aplicando filtros
            month = self.driver.find_element(By.XPATH, value='/html/body/div[3]/div/form/div/div[12]/div/input')
            month.click()
            time.sleep(5)

            try:
                current_page = self.driver.find_element(By.CLASS_NAME, "current").text
            except:
                continue
            # download pdfs
            while True:

                try:
                    for idx in range(1, 11, 1):
                        local = '/html/body/form/div/div/div[2]/div/div/div/table/tbody/tr[' + str(
                            idx) + ']/td[10]/div/a[2]'
                        month = self.driver.find_element(By.XPATH, value=local)
                        month.click()
                        time.sleep(5)
                except:
                    break

                # navegando para a página seguinte
                month = self.driver.find_element(By.XPATH, value='/html/body/form/div/div/div[2]/div/div/div/div[5]/a[2]')
                month.click()
                time.sleep(5)

                new_page = self.driver.find_element(By.CLASS_NAME, "current").text

                if new_page == current_page:
                    break
                else:
                    current_page = new_page

            while True:
                try:
                    self._move_files_from_download_to_cifii(self.temp_path, all_categorys[category - 1])
                    break
                except:
                    time.sleep(50)
        shutil.rmtree(self.temp_path)
        self.driver.quit()

    def _move_files_from_download_to_cifii(self, download_path: str, category: str):
        """
        Método para mover os dados baixados para os diretórios corretos.

        Args:
            download_path (str): path de download dos arquivos.
            category (str): nome da categoria na cvm.
        """

        for caminho, d, file in os.walk(download_path):
            for filename in file:
                source_path = os.path.join(download_path, filename)
                destination_path = os.path.join('.', "data", "data_cvm", category, filename)
                # Using os.rename():
                os.rename(source_path, destination_path) 
        
    def scrap(self) -> list:
        """
        Método para realizar o scrap dos dados.

        Returns:
            list: lista de documentos da classe langchain_core.documents.base.Document
        """

        self._download_datas()

        documents_cvm = []
        for caminho, d, file in os.walk(self.target_path):
            for filename in file:
                arquivo = os.path.join(caminho,filename)
                try:
                    if 'pdf' in str(arquivo):
                        loader = PyPDFLoader(arquivo)
                        documents_cvm.extend(loader.load())  # append ou extend (ver)
                    elif 'xml' in str(arquivo):
                        loader = UnstructuredXMLLoader(arquivo)
                        documents_cvm.extend(loader.load())
                except:
                    print("ERROR")

        return documents_cvm
