import json

import psycopg2

from blockchain.block import Block
from blockchain.vars import difficulty
from blockchain.DB import connect


def proof_of_work(block: Block):
    block.nonce = 0
    computed_hash = block.calculate_hash()
    while not computed_hash.startswith('0' * difficulty()):
        block.nonce += 1
        computed_hash = block.calculate_hash()
    return computed_hash


def is_valid_proof(block: Block, block_hash: str):
    return (block_hash.startswith('0' * block.difficulty)) and (block.calculate_hash() == block_hash)


def get_chain_from_db():
    conn = None
    cur = None
    try:
        block_list = []
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM block')

        db_block_list = cur.fetchall()
        for row in db_block_list:
            new_block = Block()
            new_block.index = row[0]
            new_block.version = row[1]
            new_block.time = row[2]
            new_block.nonce = row[3]
            new_block.hash = row[4]
            new_block.prev_hash = row[5]
            new_block.difficulty = row[6]
            new_block.data = row[7]
            block_list.append(new_block)
        return block_list
    except (Exception, psycopg2.Error) as err:
        print(err)
        raise err
    finally:
        if conn:
            cur.close()
            conn.close()


def save_block_to_db(b: Block):
    conn = None
    cur = None
    try:
        conn = connect()
        cur = conn.cursor()
        insert_query = """insert into block values(%s, %s, %s, %s, %s, %s, %s, %s);"""
        record_to_insert = (b.index, b.version, b.time, b.nonce, b.hash, b.prev_hash, b.difficulty, b.data)
        cur.execute(insert_query, record_to_insert)
        conn.commit()
    except (Exception, psycopg2.Error) as err:
        print(err)
        raise err
    finally:
        if conn:
            cur.close()
            conn.close()


class Blockchain:

    def __init__(self):
        self.new_data = []
        try:
            self.chain = get_chain_from_db()
        except (Exception, psycopg2.Error) as err:
            print(err, ' em blockchain')
            exit(0)
        if len(self.chain) == 0:
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, 'Grupo de brasileiros enviou bitcoin à Lua via rádio', "")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
        save_block_to_db(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    @property
    def n_blocks(self):
        return len(self.chain)

    def get_reversed_chain(self):
        res = self.chain.copy()
        res.reverse()
        return res

    def find_block_by_hash(self, block_hash):
        for block in self.chain:
            if block.hash == block_hash:
                return block
        return False

    def add_block(self, block: Block, proof: str):
        previous_hash = self.last_block.hash
        if previous_hash != block.prev_hash:
            print('hash do bloco anterior errado')
            return False
        if not is_valid_proof(block, proof):
            print('hash do bloco errado')
            return False
        block.hash = proof
        self.chain.append(block)
        save_block_to_db(block)
        return True

    def mine(self):
        if not self.new_data:
            print('sem dados para adicionar ao bloco')
            return False

        last_block = self.last_block

        new_indx = last_block.index + 1
        new_block = Block(index=new_indx, data=self.new_data, prev_hash=last_block.hash)

        proof = proof_of_work(new_block)

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

    def size_of_data(self):
        total_size = 0
        for block in self.chain:
            total_size += len(block.data.encode('utf-8'))
        return total_size
