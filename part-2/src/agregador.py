import sys
import json
import requests
import time
from pprint import pprint
import aiohttp
import asyncio

cached = {}

http_client = aiohttp.ClientSession()

async def split_list(product_list):
    result = {}

    for prod in product_list:
        _id = prod['productId']
        _img = prod['image']

        try:
            # 3 valid url per product
            if len(result[_id]) < 3:
                valid = await check_url(_img)
                if valid:
                    result[_id].append(_img)
        except KeyError:
            valid = await check_url(_img)
            if valid:
                result[_id] = []
                result[_id].append(_img)

    return result


def etl(result_list):

    final_list = []

    for pid in result_list.keys():
        product = {}
        product['productId'] = pid
        product['images'] = result_list[pid]
        final_list.append(product)

    return final_list

#  TODO: make async requests
async def check_url(url):
    valid = False

    if url in cached:
        return cached[url]

    r = await http_client.get(url)
    if r.status < 300:
        valid = True

    cached[url] = valid
    return valid

async def main():

    start = time.time()

    file_in = sys.argv[1]

    dict_out = [json.loads(line.rstrip('\n')) for line in open(file_in)]

    o = await split_list(dict_out)
    await http_client.close()
    final = etl(o)

    pprint(final)
    end = time.time()

    print(f'Elapsed time: {end-start}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
