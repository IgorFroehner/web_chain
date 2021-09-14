import datetime
from unittest import TestCase

from blockchain import Block
from blockchain.utils import mine


def get_block_json():
    return {
        'index': 1,
        'version': 1,
        'time': datetime.datetime.utcnow().isoformat(),
        'hash': 'hash',
        'prev_hash': 'prev_hash',
        'nonce': 0,
        'data': 'this block is a test for the constructor using json',
        'difficulty': 1
    }


class TestBlock(TestCase):

    def setUp(self) -> None:
        self.block = Block(index=1, data='data', prev_hash='prev_hash')

    def test_constructor_by_json(self):
        block_json = get_block_json()
        block_from_json = Block(**block_json)

        block = Block()
        block.index = block_json['index']
        block.version = block_json['version']
        block.time = block_json['time']
        block.hash = block_json['hash']
        block.prev_hash = block_json['prev_hash']
        block.nonce = block_json['nonce']
        block.data = block_json['data']
        block.difficulty = block_json['difficulty']

        self.assertEqual(block_from_json.calculate_hash(), block.calculate_hash())

    def test_genesis_block_hash_should_be_valid(self):
        block = Block(index=0, data='genesis', prev_hash='genesis')
        self.assertTrue(block.hash_is_valid())

    def test_block_hash_should_be_valid(self):
        self.block = mine(self.block)
        self.assertTrue(self.block.hash_is_valid())

    def test_block_hash_should_be_invalid(self):
        self.block.nonce = -4
        self.assertFalse(self.block.hash_is_valid())
