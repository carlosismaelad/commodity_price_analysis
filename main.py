from selenium import webdriver
import pandas as pd

## Vamos fazer o scraping dos valores atuais das commodities, atualizar a coluna "preço atual" da
## nossa planilha e analisar se é viável comprar ou vender  com base nos preços atuais

# Abrir o navegador
browser = webdriver.Chrome()
url = "https://www.google.com/"
browser.get(url)

# Importar a nossa base de dados
table = pd.read_excel("./commodities.xlsx")


for linha in table.index:
  
  produto = table.loc[linha, "Produto"]

  # Entra no site "melhorcambio.com"
  link = f"https://www.melhorcambio.com/{produto}-hoje"
  link = link.replace("á", "a").replace("ã", "a").replace("ó", "o").replace("õ", "o").replace("ô", "o").replace(
   "é", "e").replace("ê", "e").replace("ú", "u").replace("ç", "c")
  
  browser.get(link)

  #Pega a cotação de cada um dos produtos e converte para float
  cotacao = browser.find_element('xpath', '//*[@id="comercial"]').get_attribute("value")
  cotacao = float(cotacao.replace(".", "").replace(",", "."))

  # Preenche o preço atual do produto na base de dados
  table.loc[linha, "Preço Atual"] = cotacao
  

# Decidir o que podemos comprar
table["Comprar"] = table["Preço Atual"] < table["Preço Ideal"]
print(table)

browser.quit()

# Exportar a base de dados atualizada
table.to_excel("commodities_atualizado.xlsx", index=False)
