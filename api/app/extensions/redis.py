import redis
import os

redis_client = redis.redis(
	host=os.getenv('REDIS_HOST'),
    port=os.getenvi(int('REDIS_PORT')),
    password=os.getenv('REDIS_PASSWORD'),
    username=os.getenv('REDIS_USERNAME'),
    decode_response=True
)
