from flask import Flask
from flask import request
import requests
import json
import os

app = Flask(__name__)
dictionaryfile = 'data/specialwords.json'
def getSpecialDefinition(dictionary, word):
    result = "None - perhaps you need to create a definition"
    if os.path.exists(dictionary):
        with open(dictionary) as json_data:
            data = json.load(json_data)
            try:
                result = data[word]
            except:
                pass
    return result

def addSpecialDefinition(dictionary, word, definition):
    data = {}
    with open(dictionary, 'w+') as json_data:
        try:
            data = json.load(json_data)
        except:
            pass
        data[word] = definition
        json.dump(data, json_data)

def deleteSpecialDefinition(dictionary, word):
    result = "Could not delete: " + word
    with open(dictionary) as json_data:
        data = json.load(json_data)
        del data[word]
        result = "Deleted " + word
    with open(dictionary, 'w') as newfile:
        json.dump(data, newfile)
    return result

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
                return 'One definition for ' + word + ' is: ' + defn + '.'

@app.route("/definespecial", methods = ['POST'])
def definedi():
    # here we want to get the value of user (i.e. ?user=some-value)
    if request.method == 'POST':
        data = request.form
        word = data['text']
        defn = getSpecialDefinition(dictionaryfile, word)
        return 'The special definition for ' + word + ' is: ' + defn + '.'

@app.route("/addspecial", methods = ['POST'])
def addspecial():
    if request.method == 'POST':
        data = request.form
        worddefine = data['text']
        parts = worddefine.split('=')
        if len(parts) != 2:
            return "Your command needs to be formatted as 'word=definition' for this work."
        else:
            word = parts[0]
            definition = parts[1]
            addSpecialDefinition(dictionaryfile, word, definition)
            return "You've added that definition now, so feel free to do '/definespecial " + word + "' in Slack."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8511)
