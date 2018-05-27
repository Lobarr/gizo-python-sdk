"""Test for env"""
import pytest
import sys
import os
from robber import expect
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from gizo.env import Env, Envs

class TestEnv(object):
    def test_env(self):
        test = Env("test", "test")
        expect(test.env()).to.contain("test")

class TestEnvs(object):
    def test_envs(self):
        envs = Envs(Env("test", "test"), Env("test", "test"))
        expect(len(envs.envs)).to.equal(2)
        