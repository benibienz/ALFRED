from flask import Flask
from flask_session import Session
from core import gui

app = Flask(__name__)
app.secret_key = 'anotverysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
app.register_blueprint(gui.bp)
Session(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
