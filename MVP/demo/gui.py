import numpy as np
import pandas as pd
from flask import Blueprint, request, redirect, url_for, flash, render_template, Response
from .expert import Expert

bp = Blueprint('gui', __name__)
model = Expert()
states, actions, pred_hist, prob_hist = [], [], [], []
main_html = 'gui/simple.html'


@bp.route('/', methods=['GET', 'POST'])
def main():
    if len(states) == len(actions):
        s, pred_a, probs = model.display_next_state()
        states.append(s)
        pred_hist.append(pred_a)
        prob_hist.append(probs)
    else:
        s, pred_a, probs = states[-1], pred_hist[-1], prob_hist[-1]

    return render_template(main_html, state=s, pred_action=pred_a, probabilities=probs)


@bp.route('/act/<int:action>', methods=['POST'])
def act(action):
    actions.append(action)
    assert len(states) == len(actions), 'state action history mismatch'
    model.train(states, actions)
    return redirect(url_for('gui.main'))


@bp.route('/data', methods=['GET'])
def dump_data():
    """ Prints data to console """
    df = str(pd.read_sql_query('SELECT * FROM history', get_db()))
    print(df)
    return Response(df, status=200)

