**To run:**
* cd into ALFRED directory: `cd ALFRED`
* (optional) create virtual env: `python3 -m venv env`
* (optional) activate venv: `source env/bin/activate`
* install requirements: `pip install -r requirements.txt`
* run: `python main.py`
* see the app on a browser: http://127.0.0.1:8080/
* Ctrl + C to stop



**Notes**
* Jinja/HTML files are stored in **templates** and extend **base.html**
* The CSS styles are from UIkit and **static/style.css**
* All flask endpoints in **core/gui.py**
* Python backend in **core/expert.py**
  