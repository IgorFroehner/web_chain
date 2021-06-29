from .vars import difficulty

from datetime import datetime
from hashlib import sha256
import json


class Block:

    def __init__(self, index=-1, data='', prev_hash='', block_json: json = None):
        # from constructor parameters
        self.index = index
        self.version = 1
        self.prev_hash = prev_hash
        self.hash = ''
        self.time = datetime.utcnow().isoformat()
        self.nonce = 1
        self.data = data
        self.difficulty = difficulty()
        if index == -1 and data == '' and prev_hash == '' and block_json is not None:
            # from json
            self.index = block_json['index']
            self.version = block_json['version']
            self.prev_hash = block_json['prev_hash']
            self.hash = block_json['hash']
            self.time = block_json['time']
            self.nonce = block_json['nonce']
            self.data = block_json['data']
            self.difficulty = block_json['difficulty']

    def calculate_hash(self):
        block_dict = self.__dict__
        block_dict.pop('hash', None)
        block_string = json.dumps(block_dict, sort_keys=True, separators=(',', ':'))
        # print(block_string)
        return sha256(block_string.encode()).hexdigest()
