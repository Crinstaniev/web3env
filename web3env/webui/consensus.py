from flask import (
    Blueprint, render_template
)

consensus = Blueprint('consensus', __name__)

@consensus.route('/')
def hello():
    return render_template('consensus/index.html', name='Consensus')