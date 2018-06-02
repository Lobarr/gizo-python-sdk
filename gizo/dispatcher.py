from furl import furl

class Dispatcher:
    """ keeps information about a dispatcher node"""
    def __init__(self, url: str) -> None:
        """
        Parameters
        ----------
        url : str
            url of dispatcher node
        
        """
        self.url = url
        self.pub = None
        self.ip = None
        self.port = None
        parsed = furl(url)
        if parsed.username != None and parsed.host != None and parsed.port != None:
            self.pub = parsed.username
            self.ip = parsed.host
            self.port = parsed.port
        else:
            raise Exception("Unable to parse input url")
    def rpc(self) -> str:
        """
        Returns : str
        -------
        dispatcher node's rpc endpoint
        """
        return f"http://{self.ip}:{self.port}/rpc"
    def status(self) -> str:
        """
        Returns : str
        -------
        dispatcher nodes's status endpoint
        """
        return f"http://{self.ip}:{self.port}/status"
