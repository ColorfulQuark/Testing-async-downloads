import time
import asyncio
import requests
from collections import Counter
from aiohttp import ClientSession, TCPConnector

#==============
async def get_page_async(url: str) -> str:
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:32.0) Gecko/20100101 Firefox/32.0'}
    page = await asyncio.to_thread(requests.get, url, headers)
    return page.text

async def get_one_value_async(url: str) -> str:
    page = await get_page_async(url)
    value = page[100:150]
    return value

async def get_values_async(urls: list[str]) -> list[str]:
    values = await asyncio.gather(*[get_one_value_async(url) for url in urls])
    return values

def test_async(urls: list[str]) -> list[str]:
    values = asyncio.run(get_values_async(urls))
    return values

#==============
async def get_page_aio(url: str) -> str:
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            page = await response.read()
            return page.decode('utf-8')

async def get_one_value_aio(url:str) -> str:
    page = await(get_page_aio(url))
    value = page[100:150]
    return value

async def get_values_aio(urls: list[str]) -> list[str]:
    values = await asyncio.gather(*[get_one_value_aio(url) for url in urls])
    return values

def test_aio(urls: list[str]) -> list[str]:
    values = asyncio.run(get_values_aio(urls))
    return values

#==============
def get_page_sync(url: str) -> str:
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:32.0) Gecko/20100101 Firefox/32.0'}
    page = requests.get(url, headers=headers)
    return page.text

def get_one_value_sync(url: str) -> str:
    page = get_page_sync(url)
    value = page[100:150]
    return value

def get_values_sync(urls: list[str]) -> list[str]:
    values = []
    for url in urls:
        value = get_one_value_sync(url)
        values.append(value)
    return values

def test_sync(urls: list[str]) -> list[str]:
        values = get_values_sync(urls)
        return values

#==============

def main() -> None:
    urls = ['https://www.google.com/search?q=red', 'https://www.reddit.com',
        'https://www.google.com/search?q=green', 'https://www.youtube.com',
        'https://www.twitter.com', 'https://www.facebook.com']

    tests = [test_async, test_sync, test_aio]
    counter = Counter()
    for n in range(1, 6):
        for test in tests:
            t1 = time.perf_counter()
            values = test(urls)
            t2 = time.perf_counter()
            counter[test.__name__] += t2-t1
            print(f'{n} {test.__name__} = {t2-t1:.2f}')

    print()
    for name, secs in counter.items():
        print(f'{name} {secs:5.2f}')

if __name__ == '__main__':
    main()
