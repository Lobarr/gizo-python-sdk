"""Exec Environment Variables"""
from typing import Sequence, List, Any
class Env:
    """Exec environment variable
    Parameters
    ----------
    key : str
        key of environment variable
    value : any
        value of environment variable
    """
    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value
    def env(self) -> dict:
        """
        Returns : dict
        -------
        environment variable
        """
        return {self.key: self.value}

class Envs:
    """Exec environment variables

    Parameters
    ----------
    envs : Env
        accepts as much environment variables as you'd like
    """
    def __init__(self, *envs: Env) -> None:
        self.envs = []
        for env in envs:
            self.envs.append(env.env())
