from flask import Flask, request, jsonify
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    nametosearch = request.args.get('query')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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
        else:
            productDiscount = float(productDiscount.text.replace('\n','').replace('-','').replace('%',''))
        auchanResults.append({"name":productName,"price":productPrice,"discount":productDiscount,"source":"Auchan"})

    df = pd.DataFrame(auchanResults)
    df = df.sort_values(by=['discount'], ascending=False)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    return jsonify(df.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)
