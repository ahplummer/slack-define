from flask import request, jsonify, Flask
import os
from definewordJSON import JSONBacking
from definewordABC import AbstractBacking
from pylogger import projectLogger
import requests, json

app = Flask(__name__)
backing = None
filename = 'data/specialwords.json'

backing = JSONBacking(filename)
projectLogger().info('Standing up JSON backing at: ' + filename)

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
        try:
            jsonload = json.loads(resp.text)
            if len(jsonload) > 0:
                for defn in jsonload[0]['shortdef']:
                    return wrapJsonReturn('Official Definition for ' + word + ' is: ' + defn + '.')
        except:
            print('Error: ' + resp.text)
            return wrapJsonReturn('That word is not at Merriam/Webster, or there was some nasty exception....¯\_(ツ)_/¯')

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

@app.route("/listspecialwords", methods = ['POST'])
def listspecialwords():
    if request.method == 'POST':
        data = request.form
        try:
            total = int(data['text'])
            result = backing.listSpecialWords(total)
        except:
            result = "Use a number instead of text as a parameter..."

        return wrapJsonReturn(result)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8511)
