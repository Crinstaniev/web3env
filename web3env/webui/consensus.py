from flask import (
    Blueprint, render_template, request, flash, get_flashed_messages, current_app, globals
)

from .utils import load_consensus

consensus = Blueprint('consensus', __name__)

globals.args = dict(
    env_info=None,
    env=None,
)

@consensus.route('/')
def entry_point():
    return render_template('consensus/index.html')

@consensus.route('/build_env', methods=['POST', 'GET'])
def build_env():
    if request.method == 'POST':
        # collect data from the form
        # env config
        maximum_rounds = request.form['maximum_rounds']
        # validator config
        validator_size = request.form['validator_size']
        initial_proportion = request.form['initial_proportion']
        
        # show alert when the format is wrong
        try:
            if not maximum_rounds.isdigit():
                flash('Maximum rounds should be a positive integer.')
            if not validator_size.isdigit():
                flash('Validator size should be a positive integer.')
            if not (float(initial_proportion) > 0 and float(initial_proportion) < 1):
                flash('Initial proportion should be a float between 0 and 1.')
        except:
            flash('Please check your input.')
        
        # check if there is flash message
        if get_flashed_messages():
            return render_template('consensus/index.html')
        
        globals.args['env'] = load_consensus.load_env(
            validator_size=int(validator_size),
            initial_honest_proportion=float(initial_proportion),
            limit=int(maximum_rounds)
        )
        
        globals.args['env_info'] = globals.args['env'].get_env_info()
        
        return render_template('consensus/initialized.html', args=globals.args)
    
    return render_template('consensus/index.html')

@consensus.route('/run', methods=['POST', 'GET'])
def execute_env():
    return render_template('consensus/running.html', args=globals.args)
