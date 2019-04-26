import asyncio
import time
import argparse
from url_aggregator import Aggregate


async def main(file_in, file_out):

    start = time.time()

    # file_in = sys.argv[1]
    # file_out = sys.argv[2]

    # dict_out = [json.loads(line.rstrip('\n')) for line in open(file_in)]

    async with Aggregate() as agg:
        final = await agg.sanitize(file_in)
        agg.dump(final, file_out)
        print(f"Reqs: {agg.n_reqs}")
        print(f'Cache access: {agg.n_cache_access}')

    end = time.time()

    print(f'Elapsed time: {end-start}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dc-platform-backend-challenge - part-2 -\
                                     Author: Heitor Freitas Tancredo')
    parser.add_argument('-i', help='Input dump file', required=True,
                        dest='file_in')
    parser.add_argument('-o', help='Ouput dump file', required=True,
                        dest='file_out')
    args = vars(parser.parse_args())

    i_file = args.get('file_in')
    o_file = args.get('file_out')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(i_file, o_file))
