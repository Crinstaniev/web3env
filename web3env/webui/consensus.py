import json
import os
import threading

from flask import (Blueprint, flash, get_flashed_messages, globals, jsonify,
                   render_template, request, send_file, redirect)

from .utils import load_consensus, train_agent, visualize

consensus = Blueprint('consensus', __name__)

globals.args = dict(
    env_info=None,
    env=None,
    training_log=None
)

@consensus.route('/')
def entry_point():
    return render_template('consensus/index.html')
    # return redirect('/consensus')

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
    # invoke training using a new thread
    threading.Thread(target=train_agent.train_model, args=[globals.args['env']]).start()
    return render_template('consensus/running.html', args=globals.args)

@consensus.route('/training_log', methods=['GET'])
def get_training_log():
    # read training log from data path
    DATA_PATH = os.environ.get('DATA_PATH')
    log_file_path = os.path.join(DATA_PATH, 'a2c.json')
    try:
        with open(log_file_path, 'r') as f:
            log = json.load(f)
            return jsonify(log)
    except:
        print('No training log found.')
        return jsonify([])
    
@consensus.route('/training_status', methods=['GET'])
def training_status():
    DATA_PATH = os.environ.get('DATA_PATH')
    # check if a2c.zip exists
    if os.path.exists(os.path.join(DATA_PATH, 'a2c.zip')):
        return jsonify(dict(status='done'))
    else:
        return jsonify(dict(status='running'))
    
@consensus.route('/visualize', methods=['GET'])
def vis():
    visualize.generate_plot()
    DATA_PATH = os.environ.get('DATA_PATH')
    return send_file(os.path.join(DATA_PATH, 'honest_proportion.png'))