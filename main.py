import json

from blockchain.blockchain import Blockchain
from blockchain.block import Block

if __name__=='__main__':

    b = Blockchain()

    # print(b.get_chain_data())

    transacao1 = {
        "sender": "igor.asdf",
        "receiver": "fer.asdf",
        "amount": "20"
    }
    b.set_data([transacao1])

    if not b.mine():
        print('Erro ao minerar')

    transacao2 = {
        "sender": "igor.asdf",
        "receiver": "fer.asdf",
        "amount": "200"
    }
    b.set_data([transacao2])

    if not b.mine():
        print('Erro ao minerar')

    print(b.get_chain_data())

