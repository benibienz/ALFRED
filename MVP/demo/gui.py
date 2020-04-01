import numpy as np
import pandas as pd
from flask import Blueprint, request, redirect, url_for, flash, render_template, Response
from .db import get_db
from .expert import Expert

bp = Blueprint('gui', __name__)
model = Expert()
states, actions = [], []


def state_transform(state):
    """ Transforms state array into string or vice versa """
    if isinstance(state, str):
        return np.array([int(s) for s in state])
    else:
        return str(state)[1:-1].replace(' ', '')


@bp.route('/', methods=['GET', 'POST'])
def main():
    s, pred_a, probs = model.display_next_state()
    return render_template('gui/main.html', state=state_transform(s), pred_action=pred_a, probabilities=probs)


@bp.route('/act/<state>/<int:action>', methods=['POST'])
def act(state, action):
    db = get_db()
    db.execute('INSERT INTO history (state, action) VALUES (?, ?)', (state, action))
    db.commit()
    df = pd.read_sql_query('SELECT * FROM history', db)
    model.train([state_transform(s) for s in df['state']], df['action'].values)
    return redirect(url_for('gui.main'))


@bp.route('/data', methods=['GET'])
def dump_data():
    """ Prints data to console """
    df = str(pd.read_sql_query('SELECT * FROM history', get_db()))
    print(df)
    return Response(df, status=200)

