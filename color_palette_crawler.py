from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import os
import time

#import argparse

# 입력받은 keyword에 대한 palette를 크롤링 할 경우
'''
parser = argparse.ArgumentParser(description='python Implementation')
parser.add_argument('--keyword', type = str, default = None, help='input keyword')

args = parser.parse_args()

KEYWORD = args.keyword if args.keyword else 'cold'
'''

# 감정 형용사
KEYWORD = ['pretty', 'casual', 'romantic', 'natural', 'elegant', 'clear', 'cool', 
           'wild', 'dynamic', 'gorgeous', 'classic', 'chic', 'dandy', 'formal', 'modern']

def extract_rgb(row):
    try:
        rgb_list = [list(map(int, row[f'color_{i}'].split(','))) for i in range(1, 5+1)]
        return rgb_list
    except:
        return None

def main():
    driver = webdriver.Chrome('./chromedriver')

    for keyword in KEYWORD:
        # create folder
        try:
            if not os.path.exists(keyword):
                os.makedirs(keyword)
        except OSError:
            print ('Error: Creating directory. ' +  directory)

        print(f'{keyword} Downloading...')

        palette_df = pd.DataFrame(columns=['color_1', 'color_2', 'color_3', 'color_4', 'color_5'])
        
        #50개의 페이지에서 팔레트 크롤링
        for page in range(1, 50+1):
            url = 'https://color.adobe.com/ko/search?' + f'q={keyword}' + f'&page={page}'
            print('url = ', url, end= ' ')
            driver.get(url)

            time.sleep(8) 
            # popup창 처리
            try : 
                driver.find_element_by_xpath('//*[@id="react-spectrum-8"]/div/div[3]').click()
            except :
                print('popup 없음', end = ' ')

            time.sleep(8)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            palette_list = soup.select('body .Card__cardWrapper___FIINk')
            
            palette_rgb = []
            for palette in palette_list:
                palette_rgb.append([color['style'].split('(')[-1].split(')')[0] for color in palette.select('.Theme__theme___2NcED div')])
            print(len(palette_rgb))

            palette_tmp = pd.DataFrame(palette_rgb, columns=['color_1', 'color_2', 'color_3', 'color_4', 'color_5'])
            palette_df = pd.concat([palette_df, palette_tmp], ignore_index=True)
            
        
        print(f'{keyword} End..')

        palette_df['palette'] = palette_df.apply(extract_rgb, axis=1)

        #이미지로 다운로드
    #     for i in range(len(palette_df)):
    #         cnt += 1
    #         plt.figure(figsize=(15, 3))
    #         try :
    #             plt.imshow([palette_df.loc[i, 'palette']])
    #         except:
    #             continue
    #         plt.savefig(f'./{keyword}/{cnt}.jpg', dpi=300)

        palette_df.to_csv(f'./{keyword}/{keyword}.csv')

    driver.quit()

if __name__ == '__main__':
    main()