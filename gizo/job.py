"""Requests"""
import json
from typing import Sequence, Dict, List

class Requests:
    """Requests for tasks to be executed (multiple execs)

    Parameters
    ----------
    job_id : str
        id of job to execute
    job_exec : dict
        execs to be executed
    """
    def __init__(self, job_id: str, *execs: Dict) -> None:
        self.id: str = job_id
        self.execs: List[Dict] = []
        for e in execs:
            self.execs.append(e)
    def jrs(self) -> str:
        """
        Returns - json
        -------
        json of id and execs
        """
        return json.dumps({'ID': self.id, 'Execs': self.execs})
