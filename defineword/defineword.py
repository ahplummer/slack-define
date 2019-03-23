from flask import request, jsonify, Flask
import requests, json, os, threading, errno

mutex = threading.Lock()

app = Flask(__name__)
dictionaryfile = 'data/specialwords.json'
def getSpecialDefinition(dictionary, word):
    result = "None - perhaps you need to create a definition"
    if os.path.exists(dictionary):
        with mutex:
            with open(dictionary) as json_data:
                data = json.load(json_data)
                try:
                    result = data[word]
                except:
                    pass
    return result

def addSpecialDefinition(dictionary, word, definition):
    data = {}
    with mutex:
        if not os.path.exists(os.path.dirname(dictionary)):
            try:
                os.makedirs(os.path.dirname(dictionary))
            except:
                pass
        if os.path.exists(dictionary):
            with open(dictionary) as original_json:
                try:
                    data = json.load(original_json)
                except:
                    pass
        data[word] = definition
        with open(dictionary, 'w+') as json_data:
            json.dump(data, json_data)

def deleteSpecialDefinition(dictionary, word):
    result = "Could not delete: " + word
    with mutex:
        with open(dictionary) as json_data:
            data = json.load(json_data)
            del data[word]
            result = "Deleted " + word
        with open(dictionary, 'w') as newfile:
            json.dump(data, newfile)
        return result

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
                return wrapJsonReturn('One definition for ' + word + ' is: ' + defn + '.')

@app.route("/definespecial", methods = ['POST'])
def definedi():
    # here we want to get the value of user (i.e. ?user=some-value)
    if request.method == 'POST':
        data = request.form
        word = data['text']
        defn = getSpecialDefinition(dictionaryfile, word)
        return wrapJsonReturn('The special definition for ' + word + ' is: ' + defn + '.')

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
            return wrapJsonReturn("You've added that definition now, so feel free to do '/getspecialword " + word + "' in Slack.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8511)
