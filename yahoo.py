from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import string

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument('window-size=400,800')

driver = webdriver.Chrome(options=options, service=service)

# Navegando para a página do Yahoo Finanças com as ações mais ativas
driver.get('https://finance.yahoo.com/most-active')

# Esperando o driver carregar
driver.implicitly_wait(10)

# Obtendo o HTML da págian
html = driver.page_source

# Analisando o HTML com BeautifulSoup
site = BeautifulSoup(html, 'html.parser')

# Encontrando a tabela das ações
acoes = site.findAll('table', attrs={'class': 'tr'})
dados_acoes = []

# Analisando as informações de cada ação
for acao in acoes:
    sigla = acao.find('td')[0].text.strip()
    nome_empresa = acao.find('td')[1].text.strip()
    variacao_porcentagem = acao.find('td')[2].text.strip()
    variacao_nominal = acao.find('td')[3].text.strip()
    volume = acao.find('td')[4].text.strip()
    valor_mercado = acao.find('td')[5].text.strip()
    dados_acoes.append([sigla, nome_empresa, variacao_porcentagem,
                       variacao_nominal, volume, valor_mercado])

# Transformando a matriz de dados em uma planilha
dados = pd.DataFrame(dados_acoes, columns=[
                     'Sigla', 'Nome da empresa', 'Variação em porcentagem', 'Variação nominal', 'Volume', 'Valor de mercado'])
dados.to_csv('yahoo_acoes.csv', index=False)

driver.quit()