import sys
import json
import time
import aiohttp
import asyncio


class Aggregate:

    def __init__(self):
        self.cached = {}
        self.http_client = aiohttp.ClientSession()
        self.n_reqs = 0
        self.n_cache_access = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self.http_client.close()
        self.cached = {}

    async def sanitize(self, file_in):
        result = {}

        # for prod in product_list:
        with open(file_in) as fd:
            for line in fd:
                prod = json.loads(line.rstrip('\n'))
                _id = prod['productId']
                _img = prod['image']

                try:
                    # 3 valid url per product
                    if len(result[_id]) < 3:
                        valid = await self.__check_url(_img)
                        if valid:
                            result[_id].append(_img)
                except KeyError:
                    valid = await self.__check_url(_img)
                    if valid:
                        result[_id] = []
                        result[_id].append(_img)

        return self.__transforming(result)

    def dump(self, result_list, dump_file):
        with open(dump_file, 'a') as fd_out:
            fd_out.writelines(f"{x}\n" for x in result_list)


    def __transforming(self, result_list):

        final_list = []

        for pid in result_list.keys():
            product = {}
            product['productId'] = pid
            product['images'] = result_list[pid]
            final_list.append(product)

        return final_list

    async def __check_url(self, url):
        valid = False

        if url in self.cached:
            self.n_cache_access += 1
            return self.cached[url]

        r = await self.http_client.get(url)
        self.n_reqs += 1
        if r.status < 300:
            valid = True
        self.cached[url] = valid
        return valid



async def main():

    start = time.time()

    file_in = sys.argv[1]
    file_out = sys.argv[2]

    # dict_out = [json.loads(line.rstrip('\n')) for line in open(file_in)]

    async with Aggregate() as agg:
        final = await agg.sanitize(file_in)
        agg.dump(final, file_out)
        print(f"Reqs: {agg.n_reqs}")
        print(f'Cache access: {agg.n_cache_access}')

    end = time.time()

    print(f'Elapsed time: {end-start}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
