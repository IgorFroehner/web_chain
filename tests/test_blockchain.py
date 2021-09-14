import datetime
from math import ceil

from unittest import TestCase
from unittest.mock import MagicMock

from blockchain import Blockchain, blockchain, Block
from blockchain.utils import mine


class TestBlockchain(TestCase):

    def setUp(self) -> None:
        self.mocked_chain = []
        blockchain.block.find_all = MagicMock(return_value=self.mocked_chain)
        blockchain.block.save = self.mocked_chain.append
        blockchain.block.save(Block(index=1, hash='2', data='asdf'))
        blockchain.block.save(Block(index=2, hash='1', data='asdf'))
        self.bc = Blockchain()

    def test_should_be_a_valid_chain(self):
        self.bc.create_genesis_block()
        self.assertTrue(self.bc.validate_chain())

    def test_create_genesis_block(self):
        genesis_block = self.bc.create_genesis_block()[0]
        self.assertEqual(genesis_block.index, 0)

    def test_n_blocks(self):
        self.assertEqual(self.bc.n_blocks, 2)

    def test_find_block_by_hash(self):
        blockchain.block.find_by_hash = MagicMock(return_value=Block(hash='asdf'))

        block = self.bc.find_block_by_hash('asdf')
        self.assertEqual(block.hash, 'asdf')

    def test_add_block(self):
        self.setUp()
        block = Block(index=3, prev_hash='2')
        block = mine(block)

        self.bc.add_block(block, block.hash)
        self.assertEqual(len(self.bc._chain), 3)
        self.setUp()

    def test_size_of_data(self):
        s = 0
        for block in self.bc._chain:
            s += len(block.data.encode('utf-8'))
        self.assertEqual(self.bc.size_of_data(), s)

    def test_calculate_difficulty(self):
        self.assertEqual(self.bc.calculate_difficulty(), ceil(self.bc.calculate_difficulty()/200))


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
