"""Item Pipelines"""
import json
import os
from src.utils.redis_client import get_redis_client


class RedisPipeline:
    """Save items to Redis"""
    def __init__(self):
        self.redis_client = get_redis_client()
        self.result_key = 'spider:results'

    def process_item(self, item, spider):
        item_dict = dict(item)
        self.redis_client.rpush(self.result_key, json.dumps(item_dict))
        return item


class FilePipeline:
    """Save items to local files"""
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'output')
        os.makedirs(self.output_dir, exist_ok=True)

    def process_item(self, item, spider):
        item_dict = dict(item)
        filename = f"{hash(item['url'])}.json"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(item_dict, f, ensure_ascii=False, indent=2)
        return item