from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from blockchain.blockchain import Blockchain
from blockchain.block import Block

bc = Blockchain()


@app.route('/')
def index():
    global bc
    bc = bc.update()
    return render_template('index.html', blockchain=bc)


@app.route('/block/<block_hash>')
def block(block_hash: str):
    response_block = bc.find_block_by_hash(block_hash)
    return render_template('block.html', block=response_block)


@app.route('/add_block', methods=['GET', 'POST'])
def add_block():
    if request.method == 'POST':
        block_json = request.get_json()
        block_hash = block_json['hash']
        new_block = Block(block_json=block_json)

        bc.add_block(new_block, block_hash)

        return redirect('/')
    return render_template('new_block.html', last_block=bc.last_block)


@app.route('/difficulty')
def difficulty():
    return {'difficulty': bc.difficulty}
