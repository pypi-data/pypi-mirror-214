import urllib.parse
import urllib.request
import json

class Client:
    def __init__(self, format: str = "json", auth: tuple = None, proxy: str = None) -> None:
        """
        Create a pyResty client
        """
        self.headers = {}
        self.headers["User-Agent"] = "TurboRest/0.1.4"
        match format:
            case "json":
                self.headers["Content-Type"] = f"application/{format}"
            case "xml":
                self.headers["Content-Type"] = f"application/{format}"
            case "html":
                self.headers["Content-Type"] = f"text/{format}"
            case "text":
                self.headers["Content-Type"] = f"text/{format}"
            case _:
                self.headers["Content-Type"] = "application/json"
        if auth:
            self.headers["Authorization"] = f"{auth[0]} {auth[1]}"
        self.json = False
        if format == "json":
            self.json = True
        self.proxy = proxy
        self.success = None
        self.error = print
    
    def query(self, url: str, method: str = "GET", data: dict = None) -> urllib.request.Request:
        """
        Query a REST endpoint
        """
        if data:
            data = urllib.parse.urlencode(data)
            data = data.encode("ascii")
        if self.proxy:
            proxy = urllib.request.ProxyHandler({"http": self.proxy, "https": self.proxy})
            opener = urllib.request.build_opener(proxy)
            urllib.request.install_opener(opener)
        req = urllib.request.Request(url, data=data, headers=self.headers, method=method)
        return req
    
    def get(self, url: str) -> None:
        """
        Query a REST endpoint with GET
        """
        req = self.query(url, method="GET", data=None)
        res = self.send(req)
        if res:
            if self.json:
                res_json = json.loads(res)
                if self.success:
                    self.success(res_json)
                return res_json
            else:
                if self.success:
                    self.success(res)
                return res
        else:
            self.error("Error: No response")
        return None
        
    def post(self, url: str, data: dict = None) -> None:
        """
        Query a REST endpoint with POST
        """
        req = self.query(url, method="POST", data=data)
        res = self.send(req)
        if res:
            if self.json:
                res_json = json.loads(res)
                if self.success:
                    self.success(res_json)
                return res_json
            else:
                if self.success:
                    self.success(res)
                return res
        else:
            self.error("Error: No response")
        
    def put(self, url: str, data: dict = None) -> None:
        """
        Query a REST endpoint with PUT
        """
        req = self.query(url, method="PUT", data=data)
        res = self.send(req)
        if res:
            if self.json:
                res_json = json.loads(res)
                if self.success:
                    self.success(res_json)
                return res_json
            else:
                if self.success:
                    self.success(res)
                return res
        else:
            self.error("Error: No response")
        
    def delete(self, url: str, data: dict = None) -> None:
        """
        Query a REST endpoint with DELETE
        """
        req = self.query(url, method="DELETE", data=data)
        res = self.send(req)
        if res:
            if self.json:
                res_json = json.loads(res)
                if self.success:
                    self.success(res_json)
                return res_json
            else:
                if self.success:
                    self.success(res)
                return res
        else:
            self.error("Error: No response")
    
    def patch(self, url: str, data: dict = None) -> None:
        """
        Query a REST endpoint with PATCH
        """
        req = self.query(url, method="PATCH", data=data)
        res = self.send(req)
        if res:
            if self.json:
                res_json = json.loads(res)
                if self.success:
                    self.success(res_json)
                return res_json
            else:
                if self.success:
                    self.success(res)
                return res
        else:
            self.error("Error: No response")
        
    def send(self, req: urllib.request.Request) -> None:
        """
        Send a request
        """
        with urllib.request.urlopen(req) as res:
            return res.read().decode("utf-8")
        
    def set_header(self, key: str, value: str) -> None:
        """
        Set a header
        """
        self.headers[key] = value

    def set_headers(self, headers: dict) -> None:
        """
        Set multiple headers
        """
        for key, value in headers.items():
            self.set_header(key, value)

    def set_proxy(self, proxy: str) -> None:
        """
        Set a proxy
        """
        self.proxy = proxy

    def set_auth(self, auth: tuple) -> None:
        """
        Set an auth
        """
        self.headers["Authorization"] = f"{auth[0]} {auth[1]}"

    def set_format(self, format: str) -> None:
        """
        Set a format
        """
        self.headers["Content-Type"] = format
        self.json = False
        if format == "json":
            self.json = True

    def set_json(self, json: bool) -> None:
        """
        Set json
        """
        self.json = json
        if json:
            self.headers["Content-Type"] = "application/json"

    def set_user_agent(self, user_agent: str) -> None:
        """
        Set a user agent
        """
        self.headers["User-Agent"] = user_agent

    def set_success(self, success: callable) -> None:
        """
        Set a success callback
        """
        self.success = success