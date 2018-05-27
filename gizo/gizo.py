import requests
import hprose
import json
import sys
from os import path
from furl import furl
from gizo.centrum import CENTRUM_TESTNET, CENTRUM
from gizo.dispatcher import Dispatcher
from gizo.env import Envs
from gizo.job import JobRequest, JobRequests

class Gizo:
    """Connects to dispatcher and exposes rpc methods
    Parameters
    ----------
    url : str
        url of specific dispatcher to connect to
    export_file : str
        file for config to be written
    test_net : bool
        specifies if sdk should connect to testnet or prod network

    Raises
    ------
    Exception
        if unable to connect to centrum
        if unable to connect to a specified dispatcher
        if no dispatchers are available
    """
    def __init__(self, url: str=None, export_file: str=None, test: bool=False):
        self.__dispatcher: Dispatcher = None
        self.__client: hprose.HproseHttpClient = None
        self.__config: str = None
        self.__keys: dict = None
        self.__test: bool = test

        if export_file is None:
            if self.__test:
                self.__config = ".gizo-test"
            else:
                self.__config = ".gizo"
        else:
            self.__config = export_file
        if path.isfile(self.__config):
            try:
                self.__import_config()
                requests.get(self.__dispatcher.status(), timeout=0.5)
                self.__client = self.__connect_dispatcher(self.__dispatcher)
            except Exception:
                self.__dispatcher = None
                self.__connect()
                self.__export_config()
        else:
            if url != None:
                try:
                    self.__dispatcher = Dispatcher(url)
                    requests.get(self.__dispatcher.status(), timeout=0.5)
                    self.__client = self.__connect_dispatcher(self.__dispatcher)
                    self.__keys = self.KeyPair()
                    self.__export_config()
                except Exception:
                    raise Exception("unable to connect to dispatcher")
            else:
                self.__connect()
                self.__keys = self.KeyPair()
                self.__export_config()
    def __import_config(self):
        """Imports dispatcher and keys from config file
        Raises
        ------
        IOError
            If the file could not be read.
        """
        with open(self.__config, "r") as f:
            content = json.loads(f.read())
        self.__dispatcher = Dispatcher(content["dispatcher"])
        self.__keys = content["keys"]
    def __export_config(self):
        """Exports dispatcher and keys to config file
        Raises
        ------
        IOError
            If the file could not be written.
        """
        temp: dict = {}
        temp["dispatcher"] = self.__dispatcher.url
        temp["keys"] = self.__keys
        with open(self.__config, "w+") as f:
            f.write(json.dumps(temp))
    def __connect(self):
        """Connects to a dispatcher
        Raises
        ------
        Exception
            if no dispatchers available
            if unable to connect to centrum
        """
        r = None
        if self.__test:
            r = requests.get(f"{CENTRUM_TESTNET}/v1/dispatchers")
        else:
            r = requests.get(f"{CENTRUM}/v1/dispatchers")
        if r.status_code == 200:
            dispatchers = r.json()
            for dispatcher in dispatchers:
                try:
                    temp = Dispatcher(dispatcher)
                    self.__client = self.__connect_dispatcher(temp)
                    self.__dispatcher = temp                
                    break
                except Exception:
                    pass
            if self.__dispatcher == None:
                raise Exception("no dispatchers available")   
        else:
            raise Exception("unable to connect to centrum")
    def __connect_dispatcher(self, dispatcher: Dispatcher) -> hprose.HproseHttpClient:
        """Connects to a specified dispatcher
        Parameters
        ----------
        dispatcher : Dispatcher
            object of dispatcher to connect

        Returns : HproseHttpClient
        -------
        hprose connection
        """
        return hprose.HttpClient(uri=dispatcher.rpc())
    def __readTask(self, fn: str) -> str:
        """Reads an anko file
        Parameters
        ----------
        fn : str
            name of anko file

        Returns : str
        ------
        content of specified anko file

        Raises
        ------
        IOError
            if file could not be read
        """
        with open(fn, "r") as f:
            content = f.read()
        return content
    def Version(self) -> dict:
        """
        Returns : dict
        ------- 
        dispatcher node's version information"""
        return json.loads(self.__client.Version())
    def PeerCount(self) -> int:    
        """
        Returns : int
        -------
        the number of peers a node has"""
        return self.__client.PeerCount()
    def BlockByHash(self, hash: str) -> dict: 
        """
        Parameters
        ---------
        hash : str
            hash of block to return

        Returns : dict
        -------
        block of specified hash

        Raises
        ------
        Exception 
            if block doesn't exist in dispatchers blockchain
        """
        return json.loads(self.__client.BlockByHash(hash))
    def BlockByHeight(self, height: int) -> dict:
        """
        Parameters
        ---------
        height : int
            height of block to return

        Returns : dict
        -------
        block at specified height

        Raises
        ------
        Exception
            if block doesn't exist in dispatchers blockchain
        """
        return json.loads(self.__client.BlockByHeight(height))
    def Latest15Blocks(self) -> list:
        """
        Returns : list
        -------
        array of most recent 15 blocks
        """
        return json.loads(self.__client.Latest15Blocks())
    def LatestBlock(self) -> dict:
        """
        Returns : dict
        -------
        latest block in the blockchain
        """
        return json.loads(self.__client.LatestBlock())
    def PendingCount(self) -> int: 
        """
        Returns : int
        -------
        number of jobs waiting to be written to the bc
        """
        return self.__client.PendingCount()
    def Score(self) -> float:
        """
        Returns : float
        -------
        benchmark score of node
        """
        return self.__client.Score()
    def Peers(self) -> list:
        """
        Returns : list
        -------
        public keys of its peers
        """
        return self.__client.Peers()
    def PublicKey(self) -> str:
        """
        Returns : str
        -------
        public key of node
        """
        return self.__client.PublicKey()
    def NewJob(self, fn: str, name: str, priv: bool) -> str:
        """
        Parameters
        ---------
        fn : str
            job file
        name : str
            name of main function - entry point into job
        priv : bool
            specified if job is private / public 

        Returns : str
        -------
        id of job

        Raises
        ------
        Exception 
            if fn is not an anko file (.ank)
        """
        if fn.find(".ank") == -1:
            raise Exception("only anko files accepted")
        return self.__client.NewJob(self.__readTask(fn), name, priv, self.__keys['priv'])
    def NewExec(self, args: list=None, retries: int=None, priority: int=None, backoff: int=None, exec_time: int=None, interval: int=None, ttl: int=None, envs: Envs=None) -> dict:
        """
        Parameters
        ----------
        args : list
            parameters passed into job
        retries : int
            number of max times to run the job on fail
        priority : int
            priority of exec
        backoff : int
            time between retries (seconds)
        exec_time : int
            unix of time to when exec should should be scheduled
        interval : int
            time between periodic execs (seconds)
        ttl : int
            time limit of job running (minutes)
        envs : Envs
            environments variables provided to exec

        Returns : dict
        -------
        exec with specified config
        """
        return json.loads(self.__client.NewExec(args, retries, priority, backoff, exec_time, interval, ttl, self.__keys['pub'], json.dumps(envs.envs)))
    def WorkersCount(self) -> int:
        """
        Returns : int
        -------
        number of workers in a dispatchers standard area
        """
        return self.__client.WorkersCount()
    def WorkersCountBusy(self) -> int:
        """
        Returns : int
        -------
        number of workers in a dispatchers standard area that are busy
        """
        return self.__client.WorkersCountBusy()
    def WorkersCountNotBusy(self) -> int:
        """
        Returns : int
        -------
        number of workers in a dispatchers standard area that are not busy
        """
        return self.__client.WorkersCountNotBusy()
    def ExecStatus(self, job_id: str, exec_hash: list) -> str:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : str
        -------
        status of exec

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecStatus(job_id, exec_hash)
    def CancelExec(self, exec_hash:list):
        """
        Parameters
        -----------
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Raises
        ------
        Exception 
            if exec isn't running
        """
        return self.__client.CancelExec(exec_hash)
    def ExecTimestamp(self, job_id: str, exec_hash: list) -> int:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : int
        -------
        timestamp of exec - when the job started running (unix)

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecTimestamp(job_id, exec_hash)
    def ExecTimestampString(self, job_id: str, exec_hash: list) -> str:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : str
        -------
        timestamp of exec - when the job started running (string)

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecTimestampString(job_id, exec_hash)
    def ExecDurationNanoseconds(self, job_id: str, exec_hash: list) -> int:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : int
        -------
        duration of an exec in nanoseconds

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecDurationNanoseconds(job_id, exec_hash)
    def ExecDurationSeconds(self, job_id: str, exec_hash: list) -> float:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : float
        -------
        duration of an exec in seconds

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecDurationSeconds(job_id, exec_hash)
    def ExecDurationMinutes(self, job_id: str, exec_hash: list) -> float:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : float
        -------
        duration of an exec in minutes

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecDurationMinutes(job_id, exec_hash)
    def ExecDurationString(self, job_id: str, exec_hash: list) -> str:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : str
        -------
        duration of an exec as string

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecDurationString(job_id, exec_hash)
    def ExecArgs(self, job_id: str, exec_hash: list) -> list:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : list
        -------
        arguments of an exec

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecArgs(job_id, exec_hash)
    def ExecErr(self, job_id: str, exec_hash: list):
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns
        -------
        error of an exec - None if no error occured

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecErr(job_id, exec_hash)
    def ExecPriority(self, job_id: str, exec_hash: list) -> int:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : int
        -------
        priority of an exec

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecPriority(job_id, exec_hash)
    def ExecResult(self, job_id: str, exec_hash: list):
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns 
        -------
        result of an exec - None if error occurs

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecResult(job_id, exec_hash)
    def ExecRetries(self, job_id: str, exec_hash: list) -> int:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : int
        -------
        number of retries attempted by the worker

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecRetries(job_id, exec_hash)
    def ExecBackoff(self, job_id: str, exec_hash: list) -> float:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : float
        -------
        time between retries of an exec(seconds)

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecBackoff(job_id, exec_hash)
    def ExecExecutionTime(self, job_id: str, exec_hash: list) -> int:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : int
        -------
        scheduled time of exec (unix)

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecExecutionTime(job_id, exec_hash)
    def ExecExecutionTimeString(self, job_id: str, exec_hash: list) -> str:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : str
        -------
        scheduled time of exec (string)

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecExecutionTimeString(job_id, exec_hash)
    def ExecInterval(self, job_id: str, exec_hash: list) -> int:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : int
        -------
        time between retries of an exec(seconds)

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecInterval(job_id, exec_hash)
    def ExecBy(self, job_id: str, exec_hash: list) -> str:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : str
        -------
        public key of worker that executed the job

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecBy(job_id, exec_hash)
    def ExecTtlNanoseconds(self, job_id: str, exec_hash: list) -> int:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : int
        -------
        tll of exec (nanoseconds)

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecTtlNanoseconds(job_id, exec_hash)
    def ExecTtlSeconds(self, job_id: str, exec_hash: list) -> float:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : float
        -------
        ttl of exec (seconds)

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecTtlSeconds(job_id, exec_hash)
    def ExecTtlMinutes(self, job_id: str, exec_hash: list) -> float:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : float
        -------
        ttl of exec (minutes)

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecTtlMinutes(job_id, exec_hash)
    def ExecTtlHours(self, job_id: str, exec_hash: list) -> float:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : float
        -------
        ttl of exec (hours)

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecTtlHours(job_id, exec_hash)
    def ExecTtlString(self, job_id: str, exec_hash: list) -> str:
        """
        Parameters
        -----------
        job_id : str
            id of job exec ran 
        exec_hash : list
            byte array of exec hash - use hex_to_bytes method in utils module to convert hex to bytes

        Returns : float
        -------
        ttl of exec (string)

        Raises
        ------
        Exception 
            if unable to find exec
        """
        return self.__client.ExecTtlString(job_id, exec_hash)
    def JobQueueCount(self) -> int:
        """
        Returns : int
        -------
        number of jobs waiting to be executed

        """
        return self.__client.JobQueueCount()
    def LatestBlockHeight(self) -> int:
        """
        Returns : int
        -------
        height of latest block in the blockchain

        """
        return self.__client.LatestBlockHeight()
    def Job(self, job_id: str) -> dict:
        """
        Parameters
        ----------
        Job_id : str
            id of job to return
        Returns : dict
        -------
        job

        """
        return json.loads(self.__client.Job(job_id))
    def JobSubmisstionTimeUnix(self, job_id: str) -> int:
        """
        Parameters
        ----------
        Job_id : str
            id of job to return
        Returns : int
        -------
        submission time of job (unix)

        """
        return self.__client.JobSubmisstionTimeUnix(job_id)
    def JobSubmisstionTimeString(self, job_id: str) -> str:
        """
        Parameters
        ----------
        Job_id : str
            id of job to return
        Returns : int
        -------
        submission time of job (string)

        """
        return self.__client.JobSubmisstionTimeString(job_id)
    def IsJobPrivate(self, job_id: str) -> bool:
        """
        Parameters
        ----------
        Job_id : str
            id of job to return
        Returns : bool
        -------
        if job is  private (true) / public (false)

        """
        return self.__client.IsJobPrivate(job_id)
    def JobName(self, job_id: str) -> str:
        """
        Parameters
        ----------
        Job_id : str
            id of job to return
        Returns : str
        -------
        name of job

        """
        return self.__client.JobName(job_id)
    def JobLatestExec(self, job_id: str) -> dict:
        """
        Parameters
        ----------
        Job_id : str
            id of job to return
        Returns : dict
        -------
        latest exec of job

        """
        return json.loads(self.__client.JobLatestExec(job_id))
    def JobExecs(self, job_id: str) -> dict:
        """
        Parameters
        ----------
        Job_id : str
            id of job to return
        Returns : dict
        -------
        all execs of a job

        """
        return json.loads(self.__client.JobExecs(job_id))
    def BlockHashesHex(self) -> list:
        """
        Returns : list
        -------
        hashes of blocks in the blockchain

        """
        return self.__client.BlockHashesHex()
    def KeyPair(self) -> dict: 
        """
        Returns : dict
        -------
        pub and priv keys

        """
        return json.loads(self.__client.KeyPair())
    def Solo(self, jr: JobRequest):
        """ Executes a single exec
        Parameters
        ----------
        jr : JobRequest
            job request

        """
        return self.__client.Solo(jr.jr())
    def Chord(self, jrs: list, callback_jr: JobRequests):
        """ Executes execs one after the other then passes results into callback exec as an array (allows multiple jobs and multiple execs)
        Parameters
        ----------
        jrs : list
            array of JobRequests
        callback_jr : JobRequests
            callback job requests
        """
        return self.__client.Chord(jrs, callback_jr)
    def Chain(self, jrs: list):
        """ Executes execs one after the other (allows multiple jobs and multiple execs)
        Parameters
        ----------
        jrs : list
            array of JobRequests
        """
        return self.__client.Chain(jrs, callback_jr)
    def Batch(self, jrs: list,):
        """ Executes execs in parallel
        Parameters
        ----------
        jrs : list
            array of job requests

        Raises
        ------
        Exception
            if number of execs surpasses gizo limit
            if ttl duration surpases gizo limit
            if number of retries is greated
        """
        return self.__client.Batch(jrs, callback_jr)