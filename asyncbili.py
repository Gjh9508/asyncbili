import json
import aiohttp
import asyncio
import requests
import pandas as pd
import xlsxwriter

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").text

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

async def fetch(session, url):
    while 1:
        try:
            proxy = 'http://'+get_proxy()
            print(proxy)
            async with session.get(url,proxy = proxy) as response:
                return await response.read()
        except Exception:
            delete_proxy(proxy)

async def get_html(url,semaphore):
    async with semaphore:
        headers = {
            'Referer': 'https://www.bilibili.com/v/anime/finish/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
            }
        async with aiohttp.ClientSession(headers=headers) as session:
            html = await fetch(session, url)
            await parse_html(html)
            await asyncio.sleep(1)

async def parse_html(r):
    global data
    info = json.loads(r[38:-1])['data']['archives']
    '''df = pd.DataFrame(info)//暂时全部放在一起，部分参数扔保留了字典格式'''
    print(info[0]['aid'])
    data =data + info

def data_save(t):
    df = pd.DataFrame(t,)
    df.to_excel('bilibili.xlsx',engine='xlsxwriter')
    #pd.DataFrame.to_excel(df,)

def main():
    urls = ['https://api.bilibili.com/x/web-interface/newlist?callback=jqueryCallback_bili_09058144271712298&rid=32&type=0&pn='+str(pg)+'&ps=20&jsonp=jsonp&_=1564477907551' for pg in range(1,803)]
    semaphore = asyncio.Semaphore(20)
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(get_html(url,semaphore)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)
    data_save(data)

if __name__ == '__main__':
    data = []
    main()