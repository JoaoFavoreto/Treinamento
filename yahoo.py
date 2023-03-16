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
options.add_argument('--headless')

driver = webdriver.Chrome(options=options, service=service)

# Navegando para a página do Yahoo Finanças com as ações mais ativas
driver.get('https://finance.yahoo.com/most-active?count=100&offset=0')

time.sleep(2)

# Obtendo o HTML da página
html = driver.page_source

time.sleep(2)

# Analisando o HTML com BeautifulSoup
site = BeautifulSoup(html, 'html.parser')
acoes = site.findAll('tr', attrs={'class' : 'simpTblRow'})
detalhes_acoes = []

for acao in acoes:
    sigla = acao.find('td', attrs={'aria-label' : 'Symbol'}).text
    empresa = acao.find('td', attrs={'aria-label' : 'Name'}).text
    variacao_nominal = acao.find('td', attrs={'aria-label' : 'Change'}).text
    variacao_porcentagem = acao.find('td', attrs={'aria-label' : "% Change"}).text
    volume = acao.find('td', attrs={'aria-label' : 'Volume'}).text
    valor_mercado = acao.find('td', attrs={'aria-label' : 'Market Cap'}).text
    detalhes_acoes.append([sigla, empresa, variacao_nominal, variacao_porcentagem, volume, valor_mercado])

dados = pd.DataFrame(detalhes_acoes, columns=['Sigla', 'Nome', 'Variacao', 'Variacao em %', 'Volume', 'Valor de mercado'])

dados.to_csv('yahoo_finance.csv', index=False)
