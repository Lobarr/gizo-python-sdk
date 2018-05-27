import pytest
import sys
import os 
import base64
from robber import expect
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import gizo.priorities as priorities

class TestPriorities(object):
    def test_values(self):
        expect(priorities.HIGH).to.be.an.integer()
        expect(priorities.MEDIUM).to.be.an.integer()
        expect(priorities.LOW).to.be.an.integer()
        expect(priorities.NORMAL).to.be.an.integer()
