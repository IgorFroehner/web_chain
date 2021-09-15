from sqlalchemy import desc

from datetime import datetime
from hashlib import sha256
from typing import Optional, List
import json

from app import db


class Block(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    nonce = db.Column(db.Integer)
    prev_hash = db.Column(db.String(64))
    user = db.Column(db.String(64))
    hash = db.Column(db.String(64))
    difficulty = db.Column(db.Integer)
    data = db.Column(db.String)

    def __init__(self, **kwargs):
        self.index = kwargs.get('index', -1)
        self.version = kwargs.get('version', 1)
        self.prev_hash = kwargs.get('prev_hash')
        self.hash = kwargs.get('hash', '')
        self.time = kwargs.get('time', datetime.utcnow().isoformat())
        self.user = kwargs.get('user')
        self.nonce = kwargs.get('nonce', 0)
        self.data = kwargs.get('data')
        self.difficulty = kwargs.get('difficulty', 1)

    def calculate_hash(self) -> str:
        block_dict = self.__dict__.copy()
        block_dict.pop('hash', None)
        block_dict.pop('_sa_instance_state', None)
        block_string = json.dumps(block_dict, sort_keys=True, separators=(',', ':'), default=str)
        return sha256(block_string.encode()).hexdigest()

    def hash_is_valid(self) -> bool:
        if self.index == 0:
            return True
        return (self.hash.startswith('0' * self.difficulty)) and self.hash == self.calculate_hash()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.calculate_hash() == other.calculate_hash()
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


def save(block: Block):
    db.session.add(block)
    db.session.commit()


def find_all() -> List[Block]:
    return Block.query.order_by(desc(Block.index)).all()


def find_by_hash(hash: str) -> Optional[Block]:
    return Block.query.filter_by(hash=hash).first()
