import pytest, sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from defineword import getSpecialDefinition

def test_getSpecialDefinition():
    definition = getSpecialDefinition('beastmode')
    assert definition == "To work remotely - in a beastmode way."
