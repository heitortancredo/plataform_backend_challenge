import json
import aiohttp
import asyncio
import os


class Aggregate:

    def __init__(self):
        self.cached = {}
        self.http_client = None # aiohttp.ClientSession()
        self.n_reqs = 0
        self.n_cache_access = 0

    async def __aenter__(self):
        self.http_client = aiohttp.ClientSession()

        return self

    async def __aexit__(self, *excinfo):
        await self.http_client.close()
        self.cached = {}

    async def sanitize(self, file_in):
        result = {}

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
                    result[_id] = []
                    valid = await self.__check_url(_img)

                    if valid:
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

        #  Mockserver dont support HEAD method

        try:
            if os.environ['TEST_MODE'] == 'true':
                r = await self.http_client.get(url)
        except Exception:
            r = await self.http_client.head(url)
        self.n_reqs += 1

        if r.status < 300:
            valid = True
        self.cached[url] = valid

        return valid
