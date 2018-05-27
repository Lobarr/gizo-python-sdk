import pytest
import sys
import os
import base64
from robber import expect
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import gizo.utils as utils

_list = [116, 101, 115, 116, 105, 110, 103]

class TestUtils(object):
    def test_to_hex(self):
        expect(utils.to_hex(_list)) == '74657374696e67'
    def test_to_bytes(self):
        expect(utils.to_bytes(utils.to_hex(_list))) == _list