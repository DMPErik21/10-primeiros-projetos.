#importando bibliotecas

import requests 
from bs4 import BeautifulSoup
import csv

#Link da pagína.
URL = "https://github.com/trending"

#fazendo uma requisiçao.
requisicao = requests.get(URL)
print(requisicao)
#print(requisicao.text) #para visualizar txt.

#usando o BeautfilSoup para melhorar a aparencia do codigo html, usando o leitor 'parser'.
site = BeautifulSoup(requisicao.text, "html.parser")

# Encontrar os 10 primeiros projetos na página.
projeto = site.find_all('article', class_='Box-row')[:10]

#lista para armazenar os dados.
projeto_data = []

#extraindo o nome do projeto de cada objeto projeto, e limpando o texto.
for idx, projeto in enumerate(projeto, start=1):
    projeto_name = projeto.h2.a.get_text(strip=True).replace("\n", "").replace(" ", "")

    #extraindo a linguagem de programação.
    language = projeto.find('span', itemprop='programmingLanguage')
    language = language.get_text(strip=True) if language else "N/A"

    #extraindo o número de estrelas.
    stars = projeto.find('a', class_='Link--muted d-inline-block mr-3')
    stars = stars.get_text(strip=True).replace(',', '') if stars else "0"

    #extraindo o número de forks.
    forks = projeto.find_all('a', class_='Link--muted d-inline-block mr-3')
    forks = forks[1].get_text(strip=True).replace(',', '') if len(forks) > 1 else "0"

    #extraindo o número de estrelas do dia.
    stars_today = projeto.find('span', class_='d-inline-block float-sm-right')
    stars_today = stars_today.get_text(strip=True).split()[0].replace(',', '') if stars_today else "0"

    #adicionado os dados na lista.
    projeto_data.append([idx, projeto_name, language, stars, stars_today, forks])


    #Pecorrer a lista e imprime cada item, idivualmente.
    for data in projeto_data:
      print(data)

    Arquivo = 'GitHub.csv'

    #Escrevendo no arquivo GitHub, separado por ';', ordenado as colunas.
    with open(Arquivo, 'w', newline='', encoding='utf-8') as file:
      writer = csv.writer(file, delimiter=';')
      writer.writerow(['ranking', 'project', 'language', 'stars', 'stars today', 'forks'])
      writer.writerows(projeto_data)

