from flask import Flask
from flask import request
import requests
import json
import os

app = Flask(__name__)

@app.route("/", methods = ['POST'])
def define():
    # here we want to get the value of user (i.e. ?user=some-value)
    if request.method == 'POST':
        data = request.form
        word = data['text']
        url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/<word>?key=<apikey>"
        url = url.replace('<word>', word)
        url = url.replace('<apikey>', os.environ['apikey'])
        resp = requests.get(url)
        jsonload = json.loads(resp.text)
        if len(jsonload) > 0:
            for defn in jsonload[0]['shortdef']:
                return 'One definition for ' + word + ' is: ' + defn + '.'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8511)