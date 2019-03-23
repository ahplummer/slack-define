import pytest, sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from defineword import getSpecialDefinition, addSpecialDefinition, deleteSpecialDefinition, wrapJsonReturn

word = 'test'
definition = 'this is my test definition'
word2 = 'test2'
definition2 = 'this is my test2 definition'

dictionary = 'testfile.json'

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
    addSpecialDefinition(dictionary, word, definition)
    result = getSpecialDefinition(dictionary, word)
    assert definition == result
    addSpecialDefinition(dictionary, word2, definition2)
    result2 = getSpecialDefinition(dictionary, word2)
    assert definition2 == result2
    #ensure that first entry is still there.
    result = getSpecialDefinition(dictionary, word)
    assert definition == result

def test_getSpecialDefinition(resource_setup):
    result = getSpecialDefinition(dictionary, word)
    assert definition == result

def test_deleteSpecialDefinition(resource_setup):
    result = deleteSpecialDefinition(dictionary, word)
    assert result == "Deleted " + word

