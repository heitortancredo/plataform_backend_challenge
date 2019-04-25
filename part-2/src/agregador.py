import sys
import json
import requests
import time
from pprint import pprint

cached = {}

def unique_urls(product_list):
    unique = [dict(t) for t in set(tuple(sorted(d.items())) for d in product_list)]
    return unique

def split_list(product_list):
    result = {}

    for prod in product_list:
        _id = prod['productId']
        _img = prod['image']

        try:
            # 3 images per product
            if len(result[_id]) < 3:
                valid = check_url(_img)
                if valid:
                    result[_id].append(_img)
        except KeyError:
            result[_id] = []
            valid = check_url(_img)
            if valid:
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


def check_url(url):
    valid = False

    if url in cached:
        return cached[url]

    r = requests.get(url)
    if r.status_code < 300:
        valid = True

    cached[url] = valid
    return valid

def main():

    # start = time()
    file_in = sys.argv[1]

    dict_out = [json.loads(line.rstrip('\n')) for line in open(file_in)]

    # unique = unique_urls(dict_out)
    o = split_list(dict_out)
    final = etl(o)

    # end = time()
    # print(end-start)
    pprint(final)

if __name__ == '__main__':
    main()
