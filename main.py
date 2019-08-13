# -*- coding: utf-8 -*-
import requests
import pprint
import math
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
from io import BytesIO
import base64
import logging
import json
import os
from PIL import Image
from pytesseract import image_to_string

logging.basicConfig(filename='runtime.log', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

pp = pprint.PrettyPrinter(indent=4)

# pp.pprint(getListCity())
# print(TotalPage())

# totalPage = TotalPage()

# LIST_COM = []
# for i in range(0, totalPage):
#     print('{}/{}'.format(i+1, totalPage))
#     SUB_URL = '/api/company?l={}&p={}&r={}'.format(CITY, i+1, ROWPERPAGE)
#     r = requests.get('{}{}'.format(BASE_URL, SUB_URL))
#     result = r.json()
#     if result['LtsItems']:
#         LtsItems = result['LtsItems']
#         LIST_COM = LIST_COM + LtsItems

# df = pd.DataFrame(LIST_COM)
# df.to_excel('dac-lac.xlsx', index=False, encoding='utf-8')

# img = Image.open('/Users/toanalien/Documents/thongtindoanhnghiep-api/img.png')

# text = image_to_string(img)
results = []


def getListCompany(url):
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        # print(soup.prettify())
        searchResults = soup.select('div.search-results a')
        # for s in searchResults:
        #     print(s.attrs['href'])

        # activeTab = soup.select_one('ul.pagination li.active a')
        # if activeTab:
        #     currentPage = int(activeTab.get_text())
        #     nextPage = currentPage + 1
        ulPagination = soup.select('ul.pagination li a')
        lastLi = ulPagination[-1]
        lastLiHref = lastLi.attrs['href']
        totalPage = re.findall(
            '(?<=page\=)(.*?)(?=$)', lastLiHref)[0] if re.findall(
                '(?<=page\=)(.*?)(?=$)', lastLiHref)[0] else None
        totalPage = int(totalPage)
        logging.debug("Total page: " + str(totalPage))

        for page in range(1, totalPage + 1):
            url = 'http://www.thongtincongty.com/tinh-ninh-thuan/?page={}'.format(
                page)
            logging.info(url)
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                # print(soup.prettify())
                searchResults = soup.select('div.search-results a')
                for s in searchResults:
                    results.append(s.attrs['href'])
                logging.info(s.attrs['href'])
            time.sleep(1)
        return results
    return None


# getListCompany()

#

# with open('link.txt', 'a+') as f:
#     for i in results:
#         f.write(i + '\n')
#     f.close()

# with open('link.txt', 'r') as f:
#     arr = f.readlines()
# print(arr)
# url = 'http://www.thongtincongty.com/company/4bf56747-cong-ty-tnhh-chien-luoc-marketing-soul-va-cong-su/'
# url = 'http://www.thongtincongty.com/company/4bf570f6-cong-ty-tnhh-thuong-mai-thoi-trang-lbk/'

if __name__ == "__main__":
    # url = 'http://www.thongtincongty.com/tinh-ninh-thuan/'
    # filename = 'ninh-thuan'
    # results = getListCompany(url)
    # if results:
    #     results = list(dict.fromkeys(results))
    #     with open('link.txt', 'a+') as f:
    #         for i in results:
    #             f.write(i + '\n')
    #         f.close()
    
    
    
    
    # ==============
    
    
    flink = open('link.txt', 'r')
    arr = flink.readlines()

    # continuous fetch with cache file
    if os.path.isfile('temp.json'):
        ftemp = open('temp.json', 'r')
        results = json.load(ftemp)
    
    for idx, link in enumerate(arr):
        time.sleep(0.5)
        # try:
        try:
            print("{}/{}\t{}".format(idx, len(arr), link.strip('\n')))
            r = requests.get(link)
            content = r.content
            soup = BeautifulSoup(r.content, 'html.parser')
            info_div = soup.select_one('div.jumbotron')

            title = info_div.select_one('h4 a span')
            print(title.get_text())
            # info_div.select_one('h4').decompose()

            img = soup.select_one('div.jumbotron img')
            phone = ''
            if img:
                img = Image.open(
                    BytesIO(
                        base64.b64decode(img.attrs['src'].split(
                            'data:image/png;base64,')[1])))
                phone = image_to_string(img)
            print ("phone: ", phone)
            results.append({
                "phone": phone,
                "info": info_div.get_text(),
            })
            logging.info(link)
            arr.remove(link)
            # write backup to file json
            # except:
            #     logging.error(link)
            # time.sleep(0.5)
        except:
            with open('temp.json', 'w') as f:
                json.dump(results, f)
                f.close()
            
            with open('link.txt', 'w') as f:
                for i in arr:
                    f.write(i)
                f.close()
            exit(0)
        
        with open('temp.json', 'w') as f:
            json.dump(results, f)
            f.close()

# =======

    # with open('temp.json', 'r') as f:
    #     data = json.load(f)
    #     df = pd.DataFrame(data)
    #     df.to_excel('ninh-thuan.xlsx', index=False, encoding='utf-8')

    