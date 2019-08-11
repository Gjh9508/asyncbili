import json
import aiohttp
import asyncio
import requests
import time
import pymysql

info = []
headers = {
            'Referer': 'https://space.bilibili.com/38690046',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
            }
conn = None
cursor = None

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").text

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

async def fetch(session, url):
    while 1:
        try:
            print(url)
            proxy = get_proxy()
            proxies = 'http://'+proxy
            print(proxy)
            async with session.get(url,proxy = proxies) as response:
                return await response.read()
        except ConnectionError:
            return
        except Exception:
            delete_proxy(proxy)

async def get_html(url,semaphore):
    async with semaphore:
        async with aiohttp.ClientSession(headers=headers) as session:
            html = await fetch(session, url)
            await parse_html(html)
            await asyncio.sleep(1)

async def parse_html(r):
    global data
    try:
        data = json.loads(r)['data']
        '''df = pd.DataFrame(info)//暂时全部放在一起，部分参数扔保留了字典格式'''
        print(data['mid'])
        info.append(data)
    except Exception:
        pass

def connect_sql():
    global conn,cursor
    conn = pymysql.connect(
        host='39.104.107.179',
        port=3306,
        user='root',
        password='051414',
        database='bilibili',
        charset='utf8')
    # 获取一个光标
    cursor = conn.cursor()

def save_infos():
    global info, conn, cursor
    #print(info)
    for row in info:
        '''
        try:
            sql = 'insert into user(mid,name,sex,face,sign,rank,level,coins)\
                  values("%s","%s","%s","%s","%s","%s","%s","%s")'%(row['mid'],\
                  row['name'],row['sex'],row['face'],row['sign'],row['rank'],row['level'],row['coins'])
            cursor.execute(sql)
            conn.commit()
        except TypeError:
            conn.rollback()
        except Exception:
            pass
        '''
        try:
            sql = 'insert into user(mid,name,sex,face,sign,rank,level,coins) values("%s","%s","%s","%s","%s","%s","%s","%s")'%(row['mid'],row['name'],row['sex'],row['face'],row['sign'],row['rank'],row['level'],row['coins'])
            cursor.execute(sql)
            conn.commit()
        except Exception:
            conn.rollback()
    info = []

'''
https://github.com/zhang0peter/bilibili-video-information-spider/blob/master/new-vedio-info-spider.py
'''

if __name__ == '__main__':
    connect_sql()
    t = time.time()
    for n in range(245,300):
        urls = ['https://api.bilibili.com/x/space/acc/info?mid='+str(k) for k in range(n*10000,(n+1)*10000)]
        print(urls[1])
        semaphore = asyncio.Semaphore(200)
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(get_html(url,semaphore)) for url in urls]
        tasks = asyncio.gather(*tasks)
        loop.run_until_complete(tasks)
        save_infos()
    conn.close()
    print(time.time()-t)
