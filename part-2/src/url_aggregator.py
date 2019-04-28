import json
import aiohttp
import asyncio
import requests


class Aggregate:

    def __init__(self):
        self.cached = {}
        self.n_reqs = 0
        self.n_cache_access = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        self.cached = {}

    async def sanitize(self, file_in):
        result = {}

        with open(file_in) as fd:
            for line in fd:
                prod = json.loads(line.rstrip('\n'))
                _id = prod['productId']
                _img = prod['image']

                try:
                    result[_id].append(_img)
                except KeyError:
                    result[_id] = []
                    result[_id].append(_img)

        return await self.__transforming(result)

    def dump(self, result_list, dump_file):
        with open(dump_file, 'a') as fd_out:
            fd_out.writelines(f"{x}\n" for x in result_list)

    async def __transforming(self, result_list):

        final_list = []

        for pid in result_list.keys():
            product = {}
            product['productId'] = pid
            product['images'] = await self.__check_url(result_list[pid])
            final_list.append(product)

        return final_list

    async def __check_url(self, urls):
        url_list = []

        for url in urls:
            valid = False
            if len(url_list) == 3:
                break
            if url in self.cached and self.cached[url]:
                self.n_cache_access += 1
                url_list.append(url)
                continue

            r = requests.head(url)
            self.n_reqs += 1
            if r.status_code < 300:
                valid = True
                self.cached[url] = valid
                if valid:
                    url_list.append(url)

        return url_list

