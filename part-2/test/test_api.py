import sys
import pytest

sys.path.append("../src")
from url_aggregator import Aggregate


@pytest.mark.asyncio
async def test_sanitize_OK_n_NOK(requests_mock):
    requests_mock.head('http://test.linx/images/OK.png', status_code=200)
    requests_mock.head('http://test.linx/images/NOK.png', status_code=404)

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
async def test_sanitize_All_NOK(requests_mock):
    requests_mock.head('http://test.linx/images/NOK.png', status_code=404)

    async with Aggregate() as agg:
        result = await agg.sanitize('test_files/ALL_NOK')

    expected = [
        {'productId': 'pid2', 'images': []},
        {'productId': 'pid1', 'images': []}
    ]
    assert result == expected

@pytest.mark.asyncio
async def test_sanitize_All_OK(requests_mock):
    requests_mock.head('http://test.linx/images/OK.png', status_code=200)

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
async def test_total_requests(requests_mock):
    requests_mock.head('http://test.linx/images/OK.png', status_code=200)
    requests_mock.head('http://test.linx/images/NOK.png', status_code=404)

    async with Aggregate() as agg:
        result = await agg.sanitize('test_files/OK_NOK')

    assert agg.n_reqs == 3

@pytest.mark.asyncio
async def test_cache_size(requests_mock):
    requests_mock.head('http://test.linx/images/OK.png', status_code=200)
    requests_mock.head('http://test.linx/images/NOK.png', status_code=404)

    async with Aggregate() as agg:
        result = await agg.sanitize('test_files/OK_NOK')

    assert agg.n_cache_access == 5  # 5 url checked
