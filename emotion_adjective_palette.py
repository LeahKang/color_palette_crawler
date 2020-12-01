from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from ast import literal_eval

# 감정 형용사
KEYWORD = [
    'pretty', 'casual', 'romantic', 'natural', 'elegant', 'clear', 'cool', 
    'wild', 'dynamic', 'gorgeous', 'classic', 'chic', 'dandy', 'formal', 'modern'
    ]

def save(keyword, color, i):
    try :
        plt.figure(figsize=(15, 3))
        plt.imshow(color)
        plt.savefig(f'./{keyword}/palette/{i}.jpg', dpi=300)
    except:
        print('error')

def save_image():
    for keyword in KEYWORD:
        print('\n'+keyword)
        df = pd.read_csv(f'./{keyword}/{keyword}_drop_duplicates.csv', index_col='Unnamed: 0')

        df['palette'] = df.loc[pd.notnull(df['palette']), 'palette'].apply(literal_eval)
        
        try:
            if not os.path.exists(f'./{keyword}/palette'):
                os.makedirs(f'./{keyword}/palette')
        except OSError:
            print ('Error: Creating directory. ')

        for i in df.index:
            print(i, end=' ')
            save(keyword, [df.loc[i, 'palette']], i)

def extract_rgb(row):
    try:
        rgb_list = [list(map(int, row[f'color_{i}'].split(','))) for i in range(1, 5+1)]
        return rgb_list
    except:
        return None

def palette_crawling():
    driver = webdriver.Chrome('./chromedriver')

    for keyword in KEYWORD:
        # create folder
        try:
            if not os.path.exists(keyword):
                os.makedirs(keyword)
        except OSError:
            print ('Error: Creating directory. ' + keyword)

        print(f'{keyword} Downloading...')

        palette_df = pd.DataFrame(columns=['color_1', 'color_2', 'color_3', 'color_4', 'color_5'])
        
        for page in range(1, 25+1):
            url = 'https://color.adobe.com/ko/search?' + f'q={keyword}' + f'&page={page}'
            print('url =', url, end= ' ')
            driver.get(url)

            time.sleep(10) 
            # popup창 처리
            try : 
                driver.find_element_by_xpath('//*[@id="react-spectrum-8"]/div/div[3]').click()
            except :
                print('popup 없음', end = ' ')

            time.sleep(15)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            palette_list = soup.select('body .Card__cardWrapper___FIINk')
            
            # 모든 소스 개수
            print(len(palette_list), end = ' ')
            palette_rgb = []
            for palette in palette_list:
                if palette.select_one('.Image__image___2zb04'):
                    continue
                color5 = []
                for color in palette.select('.Theme__theme___2NcED div'):
                    color5.append(color['style'].split('(')[-1].split(')')[0])
                palette_rgb.append(color5)
            # 색상 테마 개수
            print(len(palette_rgb))
            
            palette_tmp = pd.DataFrame(palette_rgb, columns=['color_1', 'color_2', 'color_3', 'color_4', 'color_5'])
            palette_df = pd.concat([palette_df, palette_tmp], ignore_index=True)
            break
            
        print(f'{keyword} End..')

        palette_df['palette'] = palette_df.apply(extract_rgb, axis=1)

        palette_df.to_csv(f'./{keyword}/{keyword}.csv')

    driver.quit()

def main():

    palette_crawling()

    # drop_duplicates
    for keyword in KEYWORD:
        path = './'+keyword+'/'
        df = pd.read_csv(path+f'{keyword}.csv')

        values = df['palette'].value_counts().keys().tolist()
        counts = df['palette'].value_counts().tolist()

        for i in range(len(values)):
            df.loc[df['palette'] == values[i], 'count'] = counts[i]

        df_tmp = df.drop_duplicates(['palette'], keep='first')
        df_tmp.to_csv(path+f'{keyword}_drop_duplicates.csv')

        print(f'{keyword} : {len(df_tmp)}')

    save_image()

if __name__ == '__main__':
    main()