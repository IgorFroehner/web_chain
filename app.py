from flask import Flask
from flask import render_template, request, redirect
from hashlib import sha256

from blockchain.blockchain import Blockchain
from blockchain.block import Block

app = Flask(__name__)

bc = Blockchain()


@app.route('/')
def index():
    return render_template('index.html', blockchain=bc)


@app.route('/block/<block_hash>')
def block(block_hash: str):
    blck = bc.find_block_by_hash(block_hash)
    if not blck:
        return redirect('/')
    return render_template('block.html', block=blck)


@app.route('/new_block', methods=['GET', 'POST'])
def new_block():
    if request.method == 'POST':
        block_json = request.get_json()
        block_hash = block_json['hash']
        # print(block_json)
        # print(block_json['hash'])
        block_test = Block(block_json=block_json)

        bc.add_block(block_test, block_hash)

        return redirect('/')
    return render_template('new_block.html', last_block=bc.last_block)
