from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os


driver = webdriver.Chrome()
# maximizar a janela, por padrão abre reduzida
driver.maximize_window()

# Preço Bitcoin
driver.get('https://www.coingecko.com/pt')
driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[6]/div[1]/div/table/tbody/tr[1]/td[3]").click()
preco_bitcoin = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div/div[1]/div[3]/div/div[1]/span[1]/span').get_attribute("data-price-previous")

# Preço Ethereum
driver.get('https://www.coingecko.com/pt/moedas/ethereum')
preco_eth = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div/div[1]/div[3]/div/div[1]/span[1]/span').get_attribute("data-price-previous")

# Preço BNB
driver.get('https://www.coingecko.com/pt/moedas/bnb')
preco_bnb = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div/div[1]/div[3]/div/div[1]/span[1]/span').get_attribute("data-price-previous")

# Preço XRP
driver.get('https://www.coingecko.com/pt/moedas/xrp')
preco_xrp = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div/div[1]/div[3]/div/div[1]/span[1]/span').get_attribute("data-price-previous")
    

# Preço Cardano
driver.get('https://www.coingecko.com/pt/moedas/cardano')
preco_ada = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div/div[1]/div[3]/div/div[1]/span[1]/span').get_attribute("data-price-previous")


# Captando o valor do Dólar
driver.get("https://www.google.com/")
driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar")
driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
cotacao_dolar = driver.find_element_by_xpath('/html/body/div[7]/div/div[10]/div[1]/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[2]/span[1]').get_attribute('data-value')
driver.quit()

preco = pd.DataFrame([["Bitcoin",f"$ {float(preco_bitcoin):.2f} "], ["Ethereum",f"$ {float(preco_eth):.2f} "], ["BNB",f" $ {float(preco_bnb):.2f} "], ["XRP",f"$ {float(preco_xrp):.2f} "], ["Cardano",f"$ {float(preco_ada):.2f}"]], columns = ["Moedas", "Valor em Dólar"])

# Adicionando o valor em real e o dia da captação do preço
preco1 = pd.DataFrame(list(map(float, [preco_bitcoin,preco_eth,preco_bnb, preco_xrp, preco_ada]))) # => [1,2,3]
preco_dolar = pd.DataFrame(list(map(float, [cotacao_dolar])))
valor_real = [f"R$ {round(value * preco_dolar, 2)}" for index,value in preco1.iterrows()]
valor_reais = pd.Series(valor_real)
valor_reais = valor_reais.replace(to_replace = ["0\n0"," "], value = ["", ""], regex = True)
preco.insert(2, "Valor em Real", valor_reais)
preco.insert(3, "Dia", datetime.date.today())

# Script feito para rodar diariamente, o código abaixo então se lê, caso o moedas(dia-atual) não exista entao crie um arquivo
# para representar o calculo deste dia. 
# Se ele existir o código para.
if os.path.exists(f'./moedas{datetime.date.today()}.xlsx') == False:
    preco.to_excel(f'moedas{datetime.date.today()}.xlsx', index = False)
else:
    break
