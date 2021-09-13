from sqlalchemy import desc

from datetime import datetime
from hashlib import sha256
from typing import Optional, List
import json

from app import db


class Block(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime)
    nonce = db.Column(db.Integer)
    prev_hash = db.Column(db.String(64))
    hash = db.Column(db.String(64))
    difficulty = db.Column(db.Integer)
    data = db.Column(db.String)

    def __init__(self, index=-1, data='', prev_hash='', difficulty=1, block_json: json = None):
        # from constructor parameters
        self.index = index
        self.version = 1
        self.prev_hash = prev_hash
        self.hash = ''
        self.time = datetime.utcnow().isoformat()
        self.nonce = 1
        self.data = data
        self.difficulty = difficulty
        if block_json is not None:
            # from json
            self.index = block_json['index']
            self.version = block_json['version']
            self.prev_hash = block_json['prev_hash']
            self.hash = block_json['hash']
            self.time = block_json['time']
            self.nonce = block_json['nonce']
            self.data = block_json['data']
            self.difficulty = block_json['difficulty']

    def calculate_hash(self) -> str:
        block_dict = self.__dict__.copy()
        block_dict.pop('hash', None)
        block_dict.pop('_sa_instance_state', None)
        block_string = json.dumps(block_dict, sort_keys=True, separators=(',', ':'), default=str)
        return sha256(block_string.encode()).hexdigest()

    def is_valid(self) -> bool:
        if self.index == 0:
            return True
        return (self.hash.startswith('0' * self.difficulty)) and self.hash == self.calculate_hash()


def save(block: Block):
    db.session.add(block)
    db.session.commit()


def find_all() -> List[Block]:
    return Block.query.order_by(desc(Block.index)).all()


def find_by_hash(hash: str) -> Optional[Block]:
    return Block.query.filter_by(hash=hash).first()
