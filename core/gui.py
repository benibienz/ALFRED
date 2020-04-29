import os
from pathlib import Path
from flask import Blueprint, request, render_template, session, jsonify
from .recommender import Recommender, ACTION_KEYS

bp = Blueprint('gui', __name__)
home_path = Path(__file__).parent


def reset():
    """ New models, clear everything """
    # clear decision tree graph
    tree_img = home_path.joinpath('static', 'images', 'tree_graph.png')
    if os.path.isfile(tree_img):
        os.remove(tree_img)

    # init models (currently just space)
    session['models'] = {'space': Recommender(state_type='space')}


def format_space_state(state):
    """
    Formats space state for html template
    Args:
        state: list of StatVars

    Returns: list of formatted strings
    """
    return [v.get_val_str() for v in state]


def format_probs(probs):
    """
    Format probabilities array for html template
    Args:
        probs: probs array from model

    Returns: list of rounded floats
    """
    return [round(p, 2) for p in probs]


@bp.route('/', methods=['GET'])
def landing():
    """
    Landing page. Resets the models and tells the user about
    the demo. Several environment pages could be chosen from here,
    but currently we are just implementing one: space.
    """
    reset()
    return render_template('gui/landing.html')


@bp.route('/play/<env>', methods=['GET'])
def main(env):
    """
    The view for the main app.
    Currently only one environment (space) is supported,
    but other environments could be easily implemented.

    Args:
        env: 'space' is the only valid argument currently
    """
    reset()
    m = session['models'][f'{env}']
    template = f'gui/{env}.html'

    s, pred_a, probs = m.step()
    return render_template(template, env=env, state=s, actions=ACTION_KEYS)


@bp.route('/act', methods=['POST'])
def act():
    """ REST endpoint for logging an action """
    # get action from request and train model
    action = request.form['action']
    env = request.form['env']
    m = session['models']['space'] if env == 'space' else session['models']['simple']
    m.train(action)

    # step to next state and return state vector and recommended action
    s, pred_a, probs = m.step()
    state_txt = format_space_state(s) if env == 'space' else s
    return jsonify({'state': state_txt, 'pred_action': pred_a, 'probs': format_probs(probs)})
