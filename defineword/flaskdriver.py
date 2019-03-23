from flask import request, jsonify, Flask
import os
from definewordJSON import JSONBacking
from definewordABC import AbstractBacking
import requests, json

app = Flask(__name__)
backing = None
jsondictionary = 'data/specialwords.json'
if 'BACKING' in os.environ:
    if os.environ['BACKING'] == 'SHELVE':
        pass #build out the SHELVE piece here.
    else:
        backing = JSONBacking(jsondictionary)
else:
    backing = JSONBacking(jsondictionary)

def wrapJsonReturn(message):
    result = {
        "response_type": "in_channel",
        "text": message
    }
    return jsonify(result)


@app.route("/define", methods = ['POST'])
def define():
    if 'APIKEY' not in os.environ:
        return 'The server doesn''t have an APIKEY variable set, sorry.'
    # here we want to get the value of user (i.e. ?user=some-value)
    if request.method == 'POST':
        data = request.form
        word = data['text']
        url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/<word>?key=<apikey>"
        url = url.replace('<word>', word)
        url = url.replace('<apikey>', os.environ['APIKEY'])
        resp = requests.get(url)
        jsonload = json.loads(resp.text)
        if len(jsonload) > 0:
            for defn in jsonload[0]['shortdef']:
                return wrapJsonReturn('Official Definition for ' + word + ' is: ' + defn + '.')

@app.route("/getspecialword", methods = ['POST'])
def getspecialword():
    # here we want to get the value of user (i.e. ?user=some-value)
    if request.method == 'POST':
        data = request.form
        word = data['text']
        defn = backing.getSpecialDefinition(word)
        return wrapJsonReturn('The special definition for ' + word + ' is: ' + defn + '.')

@app.route("/addspecialword", methods = ['POST'])
def addspecialword():
    if request.method == 'POST':
        data = request.form
        worddefine = data['text']
        parts = worddefine.split('=')
        if len(parts) != 2:
            return "Your command needs to be formatted as 'word=definition' for this work."
        else:
            word = parts[0]
            definition = parts[1]
            backing.addSpecialDefinition(word, definition)
            return wrapJsonReturn("You've added that definition now, so feel free to do '/getspecialword " + word + "' in Slack.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8511)
