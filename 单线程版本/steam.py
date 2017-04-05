# -*- coding: utf-8 -*-
'''
    旨在爬取当前steam优惠游戏信息，包括游戏分类、评分、标签、降价幅度、优惠截止日期
'''

import time
import requests
from bs4 import BeautifulSoup
import csv


# 返回对应url的页面
def getHtmlText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


# 获取最大页面数,只运行一次
def getMaxPageNum(start_url):
    html = getHtmlText(start_url)
    soup = BeautifulSoup(html, 'html.parser')
    max_page_num = int(soup.find_all('a', onclick="SearchLinkClick( this ); return false;")[-2].text)
    return max_page_num


def getGameList(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        Games = soup.find_all('a', class_='search_result_row')
        return Games
    except Exception as e:
        print('error', str(e))


# 获得每个游戏的详细信息并存入文件
def getGameInfo(gamelist, csvWriter):
    for game in gamelist:
        try:
            name = game.find_all('span', attrs={'class':"title"})[0].text
            link = game['href']
            original_price = game.find_all('strike')[0].text.strip()
            current_price = game.find_all('div', attrs={'class':"discounted"})[0].text.replace(original_price,'').strip()
            releaseday = game.find_all('div', attrs={'class':"search_released"})[0].text
            discount = game.find_all('div', attrs={'class':"search_discount"})[0].text.strip()

            #评分不一定存在，因此使用try语句尝试抓取
            try:
                score = game.find('span', attrs={'class':"search_review_summary"})\
                    ['data-store-tooltip'].replace('<br>', '_').split('_')[0]
            except Exception as e:
                print('error score', str(e))
                score = ' '
            try:
                review = game.find('span', attrs={'class':"search_review_summary"})\
                    ['data-store-tooltip'].replace('<br>', '_').split('_')[1]
            except Exception as e:
                print('error review', str(e))
                review = ' '

            #将评分替换为中文
            scoreDict = {'Very Positive':'特别好评',
                         'Positive':'好评',
                         'Overwhelmingly Positive':'好评如潮',
                         'Overwhelmingly Negative':'差评如潮',
                         'Very Negative':"特别差评",
                         'Negative':'差评',
                         'Mostly Positive':'多半好评',
                         'Mostly Negative':'多半差评',
                         'Mixed':'褒贬不一'
                            }

            # 写入csv文件
            csvWriter.writerow([name, current_price, original_price, discount,
                                releaseday, scoreDict.get(score,'unknown'), review, link])

        except Exception as e:
            print('error', str(e))
            continue


def main():
    startTime = time.time()
    urlFile = open('url.text','r')
    urlList = urlFile.readlines()
    startUrl = urlList[0]
    baseUrl = urlList[1]

    csvFile = open('Steam.csv', 'w', encoding='utf-8',newline='')
    csvWriter = csv.writer(csvFile, delimiter=',', lineterminator='\n')
    csvWriter.writerow(['名称', '当前价格', '初始价格', '折扣',
                        '发行日期', '评分', '评测情况', '游戏主页'])

    Max_page_Num = getMaxPageNum(startUrl)
    for i in range(Max_page_Num):
        pageUrl = baseUrl + str(i + 1)
        getGameInfo(getGameList(getHtmlText(pageUrl)), csvWriter)
    csvFile.close()

    endTime = time.time()
    print('总耗时为%f秒' % round(endTime - startTime, 2))



if __name__ == '__main__':
    main()
