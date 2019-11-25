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
import requests
import json
import hashlib
import time

import objc
objc.loadBundle('CoreWLAN',
                bundle_path='/System/Library/Frameworks/CoreWLAN.framework',
                module_globals=globals())
iface = CWInterface.interface()

logging.basicConfig(filename='runtime.log', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

pp = pprint.PrettyPrinter(indent=4)

RouterUrl = "http://tplinkmifi.net"
ApiEndpoint = "/cgi-bin/web_cgi"
AuthApiEndpoint = "/cgi-bin/auth_cgi"
nonce = ""

RouterToken = ""
RouterPassword = "zaq@123"


SSID = 'thien.toan.pro'
PASS = '88888888'

def getNonce():
    payload = {"module": "authenticator", "action": 0}
    r = requests.post(url='{}{}'.format(RouterUrl, AuthApiEndpoint),
                      data=json.dumps(payload))
    return r.json()

def CalculateMD5Hash(string):
    return hashlib.md5('{}:{}'.format(string, nonce).encode()).hexdigest()

def RestartRouter(token):
    payload = {"token": token, "module": "reboot", "action": 0}
    r = requests.post(url='{}{}'.format(RouterUrl, ApiEndpoint),
                      data=json.dumps(payload))
    if r.status_code == 200:
        print(r.json())
        return r.json()
    return None

def GetRouterToken(digest):
    payload = {"module": "authenticator", "action": 1, "digest": digest}
    r = requests.post(url='{}{}'.format(RouterUrl, AuthApiEndpoint),
                      data=json.dumps(payload))
    if r.status_code == 200:
        return r.json()
    return None

def checkSSID():
    return str(iface.ssid()) == SSID

def ConnectToWifi():
    iface.disassociate()
    networks, error = iface.scanForNetworksWithName_error_(SSID, None)

    network = networks.anyObject()
    print(network)
    if not network:
        return False
    success, error = iface.associateToNetwork_password_error_(
        network, PASS, None)
    print(error)
    time.sleep(5)
    print("SSID real ", iface.ssid())
    time.sleep(5)
    if str(iface.ssid()) != SSID:
        return False
    return True

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


def getListCompany(province):
    from json.decoder import JSONDecodeError
    url = 'http://www.thongtincongty.com/tinh-{}/'.format(province)

    filename = 'list-company-{}'.format(province)

    try:
        f = open(filename, 'r')
        try:
            data = json.load(f)
        except JSONDecodeError:
            print("cannot read file")
            data = {}
    except FileNotFoundError:
        f = open(filename, 'a')
    
    

    f.close()
    
    if 'companies' not in data.keys():
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            # print(soup.prettify())
            searchResults = soup.select('div.search-results a')
            ulPagination = soup.select('ul.pagination li a')
            lastLi = ulPagination[-1]
            lastLiHref = lastLi.attrs['href']
            totalPage = re.findall(
                '(?<=page\=)(.*?)(?=$)', lastLiHref)[0] if re.findall(
                    '(?<=page\=)(.*?)(?=$)', lastLiHref)[0] else None
            totalPage = int(totalPage)
            logging.debug("Total page: " + str(totalPage))
            data['totalPage']  = totalPage
            data['currentPage'] = 1
            data['companies'] = []

    for page in range(data['currentPage'], data['totalPage'] + 1):
            print("page " + str(page))
            url = 'http://www.thongtincongty.com/tinh-{}/?page={}'.format(province, page)
            logging.info(url)
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                # print(soup.prettify())
                searchResults = soup.select('div.search-results a')
                if not searchResults: exit()
                for s in searchResults:
                    data['companies'].append(s.attrs['href'])
                logging.info(s.attrs['href'])
                data['currentPage'] = page
            f = open(filename, 'w')
            json.dump(data, f)
            f.close()
        
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
    filename = 'binh-duong'
    getListCompany(filename)
    
    # ==============

    flink = open('link.txt', 'r')
    arr = flink.readlines()

    # continuous fetch with cache file
    if os.path.isfile('temp.json'):
        ftemp = open('temp.json', 'r')
        results = json.load(ftemp)

    for idx, link in enumerate(arr):
        # time.sleep(0.5)
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
            print("phone: ", phone)
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

            # wifi controller
            while not checkSSID():
                iface = CWInterface.interface()
                iface.disassociate()
                networks, error = iface.scanForNetworksWithName_error_(
                    SSID, None)

                network = networks.anyObject()
                print(network)
                if not network:
                    exit
                success, error = iface.associateToNetwork_password_error_(
                    network, PASS, None)
                time.sleep(10)

            nonce = getNonce()['nonce']
            hash_password = CalculateMD5Hash(RouterPassword)
            get_token_result = GetRouterToken(hash_password)
            print(get_token_result)
            RestartRouter(get_token_result['token'])

            loop = 1
            while True:
                print("try " + str(loop))
                loop += 1
                if ConnectToWifi():
                    break
                time.sleep(2)

    with open('temp.json', 'w') as f:
        json.dump(results, f)
        f.close()

    with open('link.txt', 'w') as f:
        for i in arr:
            f.write(i)
        f.close()

# # # =======

# #     # with open('temp.json', 'r') as f:
# #     #     data = json.load(f)
# #     #     df = pd.DataFrame(data)
# #     #     df.to_excel('ninh-thuan.xlsx', index=False, encoding='utf-8')
