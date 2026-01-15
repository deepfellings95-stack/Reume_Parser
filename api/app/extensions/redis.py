import redis
import os
from dotenv import load_dotenv

load_dotenv()
redis_client = redis.Redis(
	host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT2')),
    password=os.getenv('REDIS_PASSWORD'),
    username=os.getenv('REDIS_USERNAME'),
    decode_responses=True
)
