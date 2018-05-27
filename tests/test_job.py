
import pytest
import sys
import os
import base64
from robber import expect
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from gizo.job import JobRequest

class TestJob(object):
    def test_jr(self):
        jr = JobRequest("test", {'test': 'test'})
        expect(jr.jr()).to.contain("ID", "Exec")