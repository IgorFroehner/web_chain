import json
from math import ceil

import psycopg2

from blockchain.block import Block
import blockchain.block as block
from app import db


def is_valid_proof(block: Block, block_hash: str):
    return (block_hash.startswith('0' * block.difficulty)) and (block.calculate_hash() == block_hash)


def get_chain_from_db():
    # TODO: validate blockchain here
    return block.find_all()


def save_block_to_db(block_instance: Block):
    block.save(block_instance)


class Blockchain:

    def __init__(self):
        self.new_data = []
        try:
            self._chain = get_chain_from_db()
        except (Exception, psycopg2.Error) as err:
            print(err, ' em blockchain')
            exit(0)
        if len(self._chain) == 0:
            self.create_genesis_block()
        self.difficulty = self.calculate_difficulty()

    def update(self):
        self._chain = get_chain_from_db()
        return self

    def create_genesis_block(self):
        genesis_block = Block(0, 'Grupo de brasileiros enviou bitcoin à Lua via rádio', "")
        genesis_block.hash = genesis_block.calculate_hash()
        self._chain.append(genesis_block)
        save_block_to_db(genesis_block)

    @property
    def last_block(self):
        return self._chain[0]

    @property
    def n_blocks(self):
        return len(self._chain)

    def get_chain(self):
        return self._chain

    def find_block_by_hash(self, block_hash):
        # TODO: maybe if have a map (hash -> indexes) dont need to go through all the chain
        for block in self._chain:
            if block.hash == block_hash:
                return block
        return False

    def add_block(self, new_block: Block, proof: str):
        previous_hash = self.last_block.hash
        if previous_hash != new_block.prev_hash:
            print('Wrong prev_hash')
        if not is_valid_proof(new_block, proof):
            print('Invalid hash of this block')
        new_block.hash = proof
        self._chain.append(new_block)
        save_block_to_db(new_block)

    def mine(self):
        if not self.new_data:
            print('sem dados para adicionar ao bloco')
            return False

        last_block = self.last_block

        new_indx = last_block.index + 1
        new_block = Block(index=new_indx, data=self.new_data, prev_hash=last_block.hash)

        proof = self.proof_of_work(new_block)

        self.add_block(new_block, proof)
        self.new_data = []
        return new_block.index

    def proof_of_work(self, block: Block):
        block.nonce = 0
        computed_hash = block.calculate_hash()
        while not computed_hash.startswith('0' * self.calculate_difficulty()):
            block.nonce += 1
            computed_hash = block.calculate_hash()
        return computed_hash

    def get_chain_data(self):
        chain_data = []
        for block in self._chain:
            chain_data.append(block.__dict__)
            # print(block.__dict__)
        return json.dumps({"length": len(chain_data), "chain": chain_data})

    def set_data(self, data: str):
        self.new_data = data

    def size_of_data(self):
        total_size = 0
        for block in self._chain:
            total_size += len(block.data.encode('utf-8'))
        return total_size

    def calculate_difficulty(self):
        # TODO: better way to calculate the difficulty
        return ceil(len(self._chain) / 200)
