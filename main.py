import requests
import json
from bs4 import BeautifulSoup

response = requests.get('https://infosimples.com/vagas/desafio/commercia/product.html')

# Armazenamento da estrutura HTML na variável "site"
site = BeautifulSoup(response.content, 'html.parser')

# Armazenamento estruturado dos dados raspados no e-commerce
dicionario_dados = {}

# TITLE
title = site.find('title').text
dicionario_dados['title'] = title

# BRAND
brand = site.find('div', attrs={'class': 'brand'}).text
dicionario_dados['brand'] = brand

# CATEGORIES
categoriesString = site.find('nav', attrs={'class': 'current-category'}).text
categories = categoriesString.split(">")
dicionario_dados['categories'] = categories

# DESCRIPTION
description = site.find('div', attrs={'class': 'proddet'})
for tag_p in description('p'):
    dicionario_dados['description'] = tag_p.text

# SKUS
skus = []
v1 = []   # Array responsável pelo armazenamento da primeira versão
version1_data = site.find('div', attrs={'class': 'card-container'})
for element in version1_data:
    if element.text != '\n':
        v1.append(element.text)
available = version1_data.find('i')
if available is None:
    v1.append(True)
skus.append(v1)


v2 = []   # Array responsável pelo armazenamento da segunda versão
not_available = site.find('div', attrs={'class': 'card not-avaliable'})
product_name = not_available.find('div', attrs={'class': 'prod-nome'}).text
v2.append(product_name)
if 'Out of stock' in not_available.text:
    v2.append('NULL')
    v2.append('NULL')
    v2.append(False)
skus.append(v2)

dicionario_dados['skus'] = skus   # Integração do Array de versões ao dicionário

# PROPERTIES
properties = []
properties_table = site.find('table', attrs={'class': 'pure-table pure-table-bordered'})
properties_data = properties_table.findAll('td')
for tag_td in properties_table('td'):
    if tag_td.text != '\n':
        properties.append(tag_td.text)
dicionario_dados['properties'] = properties

# REVIEWS
reviews = []
reviews_suja = []
comments_sections = site.find_all('div', attrs={'class': 'pure-u-21-24'})
analise_box = site.find_all('div', attrs={'class': 'analisebox'})
# print(analise_box)
for comment in analise_box:
    reviews_suja.append(comment.text)
    # reviews.append()
    reviews = [item.replace('\n', '') for item in reviews_suja]
dicionario_dados['revies'] = reviews

# REVIEWS_AVERAGE_SCORE
comments_sections = site.find('div', attrs={'id': 'comments'})
average_score_string = comments_sections.find('h4').text
average_score_array = average_score_string.split(":")
reviews_average_score = average_score_array[1]
dicionario_dados['reviews_average_score'] = reviews_average_score

# URL
dicionario_dados['url'] = 'https://infosimples.com/vagas/desafio/commercia/product.html'

json_resposta_final = json.dumps(dicionario_dados, indent=4)
with open('produto.json', 'w') as arquivo_json:
    arquivo_json.write(json_resposta_final)

