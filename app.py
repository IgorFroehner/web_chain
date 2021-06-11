from flask import Flask
from flask import render_template, request, redirect

from blockchain.blockchain import Blockchain

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
        req = request.form
        bc.set_data(req['new_block_data'])
        bc.mine()
        return redirect('/')
    return render_template('new_block.html', last_block=bc.last_block)
