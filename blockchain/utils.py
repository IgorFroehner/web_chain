
from blockchain.block import Block


def mine(block: Block) -> Block:
    block.hash = block.calculate_hash()
    while not block.hash.startswith('0' * block.difficulty):
        block.nonce += 1
        block.hash = block.calculate_hash()
    return block
