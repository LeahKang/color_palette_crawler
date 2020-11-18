import requests
from bs4 import BeautifulSoup 

keyword = input('please enter keyword : ')

host = 'https://color.adobe.com/ko/search?'
parameters = f'q={keyword}'

url = host+parameters
print(url)

html = requests.get(url)

soup = BeautifulSoup(html.content, 'html.parser')

print(soup)