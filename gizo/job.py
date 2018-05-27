"""JobRequest and JobRequests"""
import json

class JobRequest:
    """Requests for task to be executed (singled exec)

    Parameters
    ----------
    job_id : str
        id of job to execute
    job_exec : dict
        exec to be executed
    """
    def __init__(self, job_id: str, job_exec: dict):
        self.id = job_id
        self.job_exec = job_exec
    def jr(self):
        """
        Returns - json
        -------
        json of id and exec
        """
        return json.dumps({'ID': self.id, 'Exec': self.job_exec})

class JobRequests:
    """Requests for tasks to be executed (multiple execs)

    Parameters
    ----------
    job_id : str
        id of job to execute
    job_exec : dict
        execs to be executed
    """
    def __init__(self, job_id: str, *execs: dict):
        self.id = job_id
        self.execs = []
        for e in execs:
            self.execs.append(e)
    def jrs(self):
        """
        Returns - json
        -------
        json of id and execs
        """
        return json.dumps({'ID': self.id, 'Exec': self.execs})
