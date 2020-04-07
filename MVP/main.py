from flask import Flask
from core import gui

app = Flask(__name__)
app.register_blueprint(gui.bp)
app.run(host='127.0.0.1', port=8080, debug=True)