import json, os, threading
from definewordABC import AbstractBacking

class JSONBacking(AbstractBacking):
    def __init__(self, dictionaryName):
        super().__init__(dictionaryName)
        self._dictionaryName = dictionaryName
        self._mutex = threading.Lock()

    def listSpecialWords(self, total):
        result = None
        retrieved = 0
        if os.path.exists(self._dictionaryName):
            with self._mutex:
                with open(self._dictionaryName) as json_data:
                    data = json.load(json_data)
                    for key in data.keys():
                        retrieved += 1
                        if result == None:
                            result = key
                        else:
                            result = result + ', ' + key
                        if retrieved >= total:
                            break
        return result

    def getSpecialDefinition(self, word):
        super().getSpecialDefinition(word)
        result = "None - perhaps you need to create a definition"
        if os.path.exists(self._dictionaryName):
            with self._mutex:
                with open(self._dictionaryName) as json_data:
                    data = json.load(json_data)
                    try:
                        result = data[word]
                    except:
                        pass
        return result

    def addSpecialDefinition(self, word, definition):
        super().addSpecialDefinition(word, definition)
        data = {}
        with self._mutex:
            if not os.path.exists(os.path.dirname(self._dictionaryName)):
                try:
                    os.makedirs(os.path.dirname(self._dictionaryName))
                except:
                    pass
            if os.path.exists(self._dictionaryName):
                with open(self._dictionaryName) as original_json:
                    try:
                        data = json.load(original_json)
                    except:
                        pass
            data[word] = definition
            with open(self._dictionaryName, 'w+') as json_data:
                json.dump(data, json_data)

    def deleteSpecialDefinition(self, word):
        super().deleteSpecialDefinition(word)
        result = "Could not delete: " + word
        with self._mutex:
            with open(self._dictionaryName) as json_data:
                data = json.load(json_data)
                del data[word]
                result = "Deleted " + word
            with open(self._dictionaryName, 'w') as newfile:
                json.dump(data, newfile)
            return result

