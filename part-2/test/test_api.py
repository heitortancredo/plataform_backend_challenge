import sys
import pytest
from aioresponses import aioresponses

sys.path.append("../src")
from url_aggregator import Aggregate


@pytest.mark.asyncio
async def test_sanitize_OK_n_NOK():
    with aioresponses() as mocked:
        mocked.get('http://test.linx/images/OK.png', status=200)
        mocked.get('http://test.linx/images/NOK.png', status=404)
        async with Aggregate() as agg:
            result = await agg.sanitize('test_files/OK_NOK')

    expected = [
        {'productId': 'pid2', 'images': ['http://test.linx/images/OK.png',
                                         'http://test.linx/images/OK.png',
                                         'http://test.linx/images/OK.png']},
        {'productId': 'pid1', 'images': ['http://test.linx/images/OK.png',
                                         'http://test.linx/images/OK.png',
                                         'http://test.linx/images/OK.png']}
    ]
    assert result == expected

@pytest.mark.asyncio
async def test_sanitize_All_NOK():
    with aioresponses() as mocked:
        mocked.get('http://test.linx/images/NOK.png', status=404)
        async with Aggregate() as agg:
            result = await agg.sanitize('test_files/ALL_NOK')

    expected = [
        {'productId': 'pid2', 'images': []},
        {'productId': 'pid1', 'images': []}
    ]
    assert result == expected

@pytest.mark.asyncio
async def test_sanitize_All_OK():
    with aioresponses() as mocked:
        mocked.get('http://test.linx/images/OK.png', status=200)
        async with Aggregate() as agg:
            result = await agg.sanitize('test_files/ALL_OK')

    expected = [
        {'productId': 'pid2', 'images': ['http://test.linx/images/OK.png',
                                         'http://test.linx/images/OK.png',
                                         'http://test.linx/images/OK.png']},
        {'productId': 'pid1', 'images': ['http://test.linx/images/OK.png',
                                         'http://test.linx/images/OK.png',
                                         'http://test.linx/images/OK.png']}
    ]
    assert result == expected


@pytest.mark.asyncio
async def test_total_requests():
    with aioresponses() as mocked:
        mocked.get('http://test.linx/images/OK.png', status=200)
        mocked.get('http://test.linx/images/NOK.png', status=404)
        async with Aggregate() as agg:
            result = await agg.sanitize('test_files/OK_NOK')

    assert agg.n_reqs == 2

@pytest.mark.asyncio
async def test_cache_size():
    with aioresponses() as mocked:
        mocked.get('http://test.linx/images/OK.png', status=200)
        mocked.get('http://test.linx/images/NOK.png', status=404)
        async with Aggregate() as agg:
            result = await agg.sanitize('test_files/OK_NOK')

    assert agg.n_cache_access == 6  # 6 url checked
