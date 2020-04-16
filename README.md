**To run:**
1) cd into ALFRED directory: `cd ALFRED`
1) (optional) create virtual env: `python3 -m venv env`
1) (optional) activate venv: `source env/bin/activate`
1) install requirements: `pip install -r requirements.txt`
1) run: `python main.py`
1) see the app on a browser: http://127.0.0.1:8080/
1) Ctrl + C to stop

To deploy on Google Cloud App Engine:
1) Create new project on Cloud console
1) `git clone` this repo and follow steps 1 to 4 above 
1) `gcloud app create`
1) `gcloud app deploy app.yaml`


**Notes**
* Jinja/HTML files are stored in **templates** and extend **base.html**
* JQuery scripts in **templates/scripts.js**
* The CSS styles are from UIkit and **static/style.css**
* All flask endpoints in **core/gui.py**
* Python backend in **core/recommender.py**
  