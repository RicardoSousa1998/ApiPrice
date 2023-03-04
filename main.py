import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

nametosearch = input("Pesquisa?")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))



# Continente Data
contURLStart ='https://www.continente.pt/pesquisa/?q='
contURLEnd = '&search-button=&lang=null'
continenteURL = contURLStart+ nametosearch + contURLEnd
driver.get(continenteURL)
continenteResults = []
continenteContent = driver.page_source
continenteSoup = BeautifulSoup(continenteContent)
continenteProducts = continenteSoup.findAll('div', attrs={"class":"productTile"})

for product in continenteProducts:
    productName = product.find('a', attrs={"class":"ct-tile--description"}).text
    productPrice = product.find('span', attrs={"class":"value"}).text.replace('\n','').replace('/un','').replace('€','').replace(',','.').replace('/Kg','').replace('\t','')
    productDiscount = product.find('span', attrs={"class":"ct-product-tile-badge-value--pvpr"})
    if productDiscount == None:
        productDiscount = float('0')
        #continue
    else:
        productDiscount = float(productDiscount.text.replace('\n',''))
    continenteResults.append({"name":productName,"price":productPrice,"discount":productDiscount,"source":"Continente"})
# Auchan Data

auchanURLStart = 'https://www.auchan.pt/pt/pesquisa?q='
auchanURLEnd = '&search-button=&lang=null'
auchanURL = auchanURLStart + nametosearch + auchanURLEnd
driver.get(auchanURL)
auchanResults = []
auchanContent = driver.page_source
auchanSoup = BeautifulSoup(auchanContent)
auchanProducts = auchanSoup.findAll('div', attrs={"class":"auc-product"})

for product in auchanProducts:
    productName = product.find('a', attrs={"class":"link"}).text
    productPrice = product.find('span', attrs={"class":"sales"}).find('span', attrs={"class":"value"}).text.replace('\n','').replace('/un','').replace('€','').replace(',','.').replace('/Kg','').replace('\t','')
    productDiscount = product.find('div', attrs={"class":"auc-promo--discount auc-promo--discount--red"})
    if productDiscount == None:
        productDiscount = float('0')
        #continue
    else:
        productDiscount = float(productDiscount.text.replace('\n','').replace('-','').replace('%',''))
    auchanResults.append({"name":productName,"price":productPrice,"discount":productDiscount,"source":"Auchan"})
# Minipreco Data

miniprecoURLStart = 'https://www.minipreco.pt/search?text='
miniprecoURLEnd = '&x=0&y=0'

miniprecoURL = miniprecoURLStart + nametosearch + miniprecoURLEnd

driver.get(miniprecoURL)
miniprecoResults = []
miniprecoContent = driver.page_source
miniprecoSoup = BeautifulSoup(miniprecoContent)
miniprecoProducts = miniprecoSoup.findAll('div', attrs={"class":"product-list__item"})

for product in miniprecoProducts:
    productName = product.find('span', attrs={"class":"details"}).text.replace('\n','').replace('\t','')
    productPrice = product.find('p', attrs={"class":"price"}).text.replace('\n','').replace('/un','').replace('€','').replace(',','.').replace('/Kg','').replace('\t','')
    productDiscount = product.find('span', attrs={"class":"label_text"})
    if productDiscount == None:
        productDiscount = float('0')
        #continue
    else:
        productDiscount = float('1')
    miniprecoResults.append({"name":productName,"price":productPrice,"discount":productDiscount,"source":"MiniPreco"})

    allResults = continenteResults + auchanResults + miniprecoResults
df = pd.DataFrame(continenteResults)
df = df.sort_values(by=['discount'], ascending=False)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
print(df)
