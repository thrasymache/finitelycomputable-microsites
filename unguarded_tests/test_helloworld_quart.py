import re
import pytest

from finitelycomputable import helloworld_quart


@pytest.mark.asyncio
async def test_helloworld_quart():
    '''helloworld test that can handle adapters'''
    client = helloworld_quart.application.test_client()
    response = await client.get('/')
    assert 200 == response.status_code
    data = await response.get_data()
    assert re.search(b'says "hello, world"\n', data)
    assert re.search(b'Quart', data)

@pytest.mark.xfail
@pytest.mark.asyncio
async def test_helloworld_quart_exact():
    '''helloworld test for exact text'''
    client = helloworld_quart.application.test_client()
    response = await client.get('/')
    assert 200 == response.status_code
    data = await response.get_data()
    assert data == b'Quart says "hello, world"\n'
