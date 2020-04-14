from flask import Flask
from core import gui

app = Flask(__name__)
app.register_blueprint(gui.bp)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)