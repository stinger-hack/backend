import asyncio
from elasticsearch import AsyncElasticsearch

ELASTIC_TOKEN = 'My_deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDY1ODdiZGRjOGFiNTQwMjE5Mzc2MjcwMDQ5MTlkYjg5JDYwZWI2MWQ3MGU2MjRkY2ZhOGY5MDcyZDNiYzExN2Uz'
ELASTIC_USER = 'elastic'
ELASTIC_PASSWORD = 'VQnUzIajNvgzp25Id9KzA0A0'

client = AsyncElasticsearch(
    cloud_id=ELASTIC_TOKEN, http_auth=(ELASTIC_PASSWORD, ELASTIC_PASSWORD))


async def elastic_info():
    resp = await client.info()


asyncio.get_event_loop().run_until_complete(elastic_info())
