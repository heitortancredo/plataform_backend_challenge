import sys
import asyncio
import time
from url_aggregator import Aggregate


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
