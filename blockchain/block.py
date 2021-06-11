from .vars import difficulty
from datetime import datetime
from hashlib import sha256
import json


class Block:

    def __init__(self, index, data, prev_hash):
        self.index = index
        self.version = 1
        self.prev_hash = prev_hash
        self.hash = ''
        self.time = datetime.utcnow().isoformat()
        self.nonce = 1
        self.data = data
        self.difficulty = difficulty()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        while not self.hash.startswith('0' * self.difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()
