from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
from skimage import io
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser(description='python Implementation')

parser.add_argument('--keyword', type = str, default = None, help='input keyword')

args = parser.parse_args()

#print(args.keyword)

KEYWORD = args.keyword if args.keyword else 'cute'
#KEYWORD = []

def main():
    driver = webdriver.Chrome('./chromedriver')
    url = 'https://color.adobe.com/ko/search?' + f'q={KEYWORD}'
    driver.get(url)
    
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="react-spectrum-8"]/div/div[3]').click()

    driver.implicitly_wait(20)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    print(soup)

    pallete_list = soup.select('body .Card__cardWrapper___FIINk')

    print(pallete_list[0])

    driver.quit()

if __name__ == '__main__':
    main()