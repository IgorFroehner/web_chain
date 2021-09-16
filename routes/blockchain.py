from flask import render_template, request, redirect
from flask import Blueprint
from flask_login import login_required

blue = Blueprint('blockchain', __name__, static_folder='static', template_folder='templates')


@blue.route('/')
def index():
    from blockchain import Blockchain
    return render_template('index.html', blockchain=Blockchain())


@blue.route('/block/<block_hash>')
def block(block_hash: str):
    from blockchain import Blockchain
    bc = Blockchain()
    response_block = bc.find_block_by_hash(block_hash)
    return render_template('block.html', block=response_block)


@blue.route('/add_block', methods=['GET', 'POST'])
@login_required
def add_block():
    from blockchain import Blockchain
    from blockchain import Block
    bc = Blockchain()
    if request.method == 'POST':
        block_json = request.get_json()
        block_hash = block_json['hash']
        new_block = Block(**block_json)

        bc.add_block(new_block, block_hash)

        return redirect('/')
    return render_template('new_block.html', last_block=bc.last_block)


@blue.route('/difficulty')
def difficulty():
    from blockchain import Blockchain
    bc = Blockchain()
    return {'difficulty': bc.calculate_difficulty()}
