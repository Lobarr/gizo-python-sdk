import pytest
import sys
import os
from robber import expect
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from gizo.dispatcher import Dispatcher

url = "gizo://304e301006072a8648ce3d020106052b81040021033a0004f14a7b28af6fdf3136779e0a82e618d5f481ab0377222e71c9473e552785eb4adedfb67030b15ba1d877f9e1a06dd8a58870dd1402da7e6e@99.233.0.99:9995"
test = Dispatcher(url)

class TestDispatcher(object):       
    def test_variables(self):
        expect(url).to.equal(test.url)
        expect(test.pub).to.be.a.string()
        expect(test.port).to.be.an.integer()
        expect(test.ip).not_to.be.none()
    def test_rpc(self):
        expect(test.rpc()) == "http://99.233.0.99:9995/rpc"
