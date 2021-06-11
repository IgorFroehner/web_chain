import json

from blockchain.block import Block
from blockchain.vars import difficulty


class Blockchain:

    def __init__(self):
        self.new_data = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, 'Grupo de brasileiros enviou bitcoin à Lua via rádio', "")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def proof_of_work(self, block: Block):
        block.nonce = 0
        computed_hash = block.calculate_hash()
        while not computed_hash.startswith('0' * difficulty()):
            block.nonce += 1
            computed_hash = block.calculate_hash()
        return computed_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @property
    def n_blocks(self):
        return len(self.chain)

    def find_block_by_hash(self, hash):
        for block in self.chain:
            if block.hash == hash:
                return block
        return False

    def add_block(self, block: Block, proof: str):
        previous_hash = self.last_block.hash
        if previous_hash != block.prev_hash:
            print('hash do bloco anterior errado')
            return False
        if not self.is_valid_proof(block, proof):
            print('hash do bloco errado')
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block: Block, block_hash: str):
        return (block_hash.startswith('0' * block.difficulty)) and (block.calculate_hash() == block_hash)

    def mine(self):
        if not self.new_data:
            print('sem dados para adicionar ao bloco')
            return False

        last_block = self.last_block

        new_indx = last_block.index+1
        new_block = Block(index=new_indx, data=self.new_data, prev_hash=last_block.hash)

        proof = self.proof_of_work(new_block)

        self.add_block(new_block, proof)
        self.new_data = []
        return new_block.index

    def get_chain_data(self):
        chain_data = []
        for block in self.chain:
            chain_data.append(block.__dict__)
            # print(block.__dict__)
        return json.dumps({"length": len(chain_data), "chain": chain_data})

    def set_data(self, data: str):
        self.new_data = data
