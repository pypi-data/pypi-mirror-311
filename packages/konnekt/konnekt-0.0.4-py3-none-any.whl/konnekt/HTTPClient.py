import socket
import json
import time
from urllib.parse import urlencode
import base64
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("http_client.log"),logging.StreamHandler()],
)

class ConnectionManager:
    def __init__(self, host, port=80, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.connect()
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect((self.host, self.port))
        logging.info(f"Connected to {self.host}:{self.port}")
    
    def send_request(self, request_data):
        logging.info("Sending request:\n" + request_data)
        self.socket.sendall(request_data.encode())
        response_data = b""
        while True:
            try:
                chunk = self.socket.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            except socket.timeout:
                break
        logging.info("Response received.")
        return response_data.decode()
    
    def close(self):
        self.socket.close()
        logging.info(f"Connection to {self.host}:{self.port} closed.")

class RequestBuilder:
    def __init__(self, method, path, headers=None, params=None, body=None):
        self.method = method.upper()
        self.path = path
        self.headers = headers or {}
        self.params = params or {}
        self.body = body or {}

    def build_request(self):
        if self.params:
            self.path += '?' + urlencode(self.params)

        if "Host" not in self.headers:
            self.headers["Host"] = "jsonplaceholder.typicode.com"

        self.headers.setdefault("User-Agent", "CustomHTTPClient/1.0")
        self.headers.setdefault("Accept", "application/json")

        body_data = ""
        if isinstance(self.body, dict):
            body_data = json.dumps(self.body)
            self.headers["Content-Type"] = "application/json"

        self.headers["Content-Length"] = str(len(body_data))

        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"
        header_lines = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())

        return f"{request_line}{header_lines}\r\n{body_data}"

class ResponseParser:
    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.headers = {}
        self.body = None
        self.status_code = None
        self.parse_response()

    def parse_response(self):
        header, _, body = self.raw_response.partition('\r\n\r\n')
        status_line, *header_lines = header.splitlines()
        self.status_code = int(status_line.split()[1])
        for line in header_lines:
            if ": " in line:
                key, value = line.split(": ", 1)
                self.headers[key] = value.strip()
        self.body = body
        logging.info(f"Response parsed: Status code {self.status_code}")

    def get_json(self):
        try:
            return json.loads(self.body)
        except json.JSONDecodeError:
            return None

class AuthManager:
    def __init__(self):
        self.auth_headers = {}

    def set_basic_auth(self, username, password):
        auth_str = f"{username}:{password}".encode("utf-8")
        auth_header = "Basic " + base64.b64encode(auth_str).decode("utf-8").strip()
        self.auth_headers["Authorization"] = auth_header
    
    def set_bearer_token(self, token):
        self.auth_headers["Authorization"] = f"Bearer {token}"

class RateLimiter:
    def __init__(self, rate=1):
        self.rate = rate  # requests per second
        self.last_request_time = 0

    def limit(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < (1 / self.rate):
            time.sleep((1 / self.rate) - time_since_last_request)
        self.last_request_time = time.time()

class CacheManager:
    def __init__(self):
        self.cache = {}

    def get_cached_response(self, request_key):
        return self.cache.get(request_key)

    def cache_response(self, request_key, response):
        self.cache[request_key] = response

class HTTPClient:
    def __init__(self, host, port=80):
        self.host = host
        self.port = port
        self.connection = ConnectionManager(host, port)
        self.rate_limiter = RateLimiter()
        self.auth_manager = AuthManager()
        self.cache_manager = CacheManager()
        self.history = []
    
    def request(self, method, path, headers=None, params=None, body=None, cache=True, retries=3):
        headers = headers or {}
        headers.update(self.auth_manager.auth_headers)
        
        request = RequestBuilder(method, path, headers=headers, params=params, body=body)
        request_data = request.build_request()
        
        cache_key = f"{method}:{path}:{params}"
        cached_response = self.cache_manager.get_cached_response(cache_key)
        if cache and cached_response:
            logging.info("Returning cached response.")
            return cached_response
        
        attempt = 0
        while attempt < retries:
            try:
                self.rate_limiter.limit()
                raw_response = self.connection.send_request(request_data)
                response = ResponseParser(raw_response)
                if cache:
                    self.cache_manager.cache_response(cache_key, response)
                self.history.append((request_data, response))
                return response
            except Exception as e:
                attempt += 1
                logging.error(f"Attempt {attempt} failed: {e}")
        
        logging.error("Request failed after retries.")
        return None
    
    def get(self, path, headers=None, params=None):
        return self.request("GET", path, headers=headers, params=params)
    
    def post(self, path, headers=None, params=None, body=None):
        return self.request("POST", path, headers=headers, params=params, body=body)
    
    def put(self, path, headers=None, params=None, body=None):
        return self.request("PUT", path, headers=headers, params=params, body=body)
    
    def delete(self, path, headers=None, params=None):
        return self.request("DELETE", path, headers=headers, params=params)
    
    def set_basic_auth(self, username, password):
        self.auth_manager.set_basic_auth(username, password)
    
    def set_bearer_token(self, token):
        self.auth_manager.set_bearer_token(token)

    def close(self):
        self.connection.close()
