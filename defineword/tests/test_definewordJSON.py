import pytest, sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from definewordJSON import JSONBacking

word = 'test'
definition = 'this is my test definition'
word2 = 'test2'
definition2 = 'this is my test2 definition'

dictionary = 'testfile.json'
jsonBacking = JSONBacking(dictionary)

@pytest.fixture(scope='module')
def resource_setup(request):
    print('Setting up resources for testing')
    if os.path.exists(dictionary):
        os.remove(dictionary)
    def resource_teardown():
        print('Tearing down resources from testing')
        if os.path.exists(dictionary):
            os.remove(dictionary)
    request.addfinalizer(resource_teardown)

def test_addSpecialDefinition(resource_setup):
    jsonBacking.addSpecialDefinition(word, definition)
    result = jsonBacking.getSpecialDefinition(word)
    assert definition == result
    jsonBacking.addSpecialDefinition(word2, definition2)
    result2 = jsonBacking.getSpecialDefinition(word2)
    assert definition2 == result2
    #ensure that first entry is still there.
    result = jsonBacking.getSpecialDefinition(word)
    assert definition == result

def test_getSpecialDefinition(resource_setup):
    result = jsonBacking.getSpecialDefinition(word)
    assert definition == result

def test_deleteSpecialDefinition(resource_setup):
    result = jsonBacking.deleteSpecialDefinition(word)
    assert result == "Deleted " + word

