import json
from math import ceil
from typing import List, Optional

from sqlalchemy import exc

from blockchain.block import Block
import blockchain.block as block
from exceptions import BlockchainException


def is_valid_proof(block: Block, block_hash: str) -> bool:
    return (block_hash.startswith('0' * block.difficulty)) and (block.calculate_hash() == block_hash)


def get_chain_from_db() -> List[Block]:
    return block.find_all()


def save_block_to_db(block_instance: Block):
    block.save(block_instance)


class Blockchain:

    def __init__(self):
        self._chain = self.init_chain()
        self.validate_chain()

    def update(self):
        self._chain = get_chain_from_db()
        return self

    def init_chain(self) -> List[Block]:
        chain = []
        try:
            chain = get_chain_from_db()
        except (Exception, exc.SQLAlchemyError) as err:
            print(err, ' in blockchain')
            exit(0)
        if len(chain) == 0:
            chain = self.create_genesis_block()
        return chain

    def validate_chain(self) -> bool:
        for block in self._chain:
            if not block.hash_is_valid():
                return True
        return False

    def create_genesis_block(self) -> List[Block]:
        genesis_block = Block(index=0, data='Grupo de brasileiros enviou bitcoin à Lua via rádio', prev_hash="")
        genesis_block.hash = genesis_block.calculate_hash()
        chain = [genesis_block]
        save_block_to_db(genesis_block)
        return chain

    @property
    def last_block(self) -> Block:
        return self._chain[0]

    @property
    def n_blocks(self) -> int:
        return len(self._chain)

    def get_chain(self) -> List[Block]:
        return self._chain

    def find_block_by_hash(self, block_hash) -> Optional[Block]:
        return block.find_by_hash(block_hash)

    def add_block(self, new_block: Block, proof: str):
        self.validate_new_block(new_block, proof)
        new_block.hash = proof
        save_block_to_db(new_block)
        self._chain = get_chain_from_db()

    def validate_new_block(self, new_block: Block, proof: str):
        previous_hash = self.last_block.hash
        if previous_hash != new_block.prev_hash:
            raise BlockchainException(f'Invalid prev_hash to the new block to be added: Block {new_block.index}'
                                      f' prev_hash should be {previous_hash} but was {new_block.prev_hash}')
        if new_block.difficulty != self.calculate_difficulty():
            raise BlockchainException(f'Wrong difficulty for the new block, it should be {self.calculate_difficulty()}')
        if not is_valid_proof(new_block, proof):
            raise BlockchainException(f'Invalid proof of work in te new block to be added: Block {new_block.index}')


    def get_chain_data(self):
        chain_data = [block.__dict__ for block in self._chain]
        return json.dumps({"length": len(chain_data), "chain": chain_data})

    def size_of_data(self):
        total_size = 0
        for block in self._chain:
            total_size += len(block.data.encode('utf-8'))
        return total_size

    def calculate_difficulty(self):
        return ceil(len(self._chain) / 10)
