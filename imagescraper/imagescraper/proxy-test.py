# THIS CODE CHECKS AGAINST A LIST OF PROXIES (https://free-proxy-list.net/) TO RETURN
# ONLY THE ONES THAT GIVE A 200 RESPONSE AND STORES THEM LOCALLY PROXY LIST TEXTFILE
# HEAVILY BASED ON https://www.youtube.com/watch?v=vJwcW2gCCE4 BUT COMBINED WITH ANOTHER
# PROXY LIST WEBSITE
# CREATED BY NATHALIE DESCUSSE-BROWN AND UPDATED 16/01/21
import requests
from bs4 import BeautifulSoup
import random
import concurrent.futures
import time

#get the list of free proxies
def getProxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text =='elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies



def extract(proxy):
    #this was for when we took a list into the function, without conc futures.
    #proxy = random.choice(proxylist)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        #change the url to https://httpbin.org/ip that doesnt block anything
        r = requests.get('https://httpbin.org/ip', headers=headers, proxies={'http' : proxy,'https': proxy}, timeout=1)
        print(r.json(), r.status_code)
        proxy_list2.write(proxy + "\n")
    except:
        pass
    return proxy


proxylist = getProxies()
print(len(proxylist))

proxy_list2 = open("proxy-list2.txt", "w")
#check them all with futures super quick
with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(extract, proxylist)

proxy_list2.close()