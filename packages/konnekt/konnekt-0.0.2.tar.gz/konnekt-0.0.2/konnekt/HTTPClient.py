import socket
import json
import time
import logging
from urllib.parse import urlencode
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("http_client.log"),  # Write logs to a file
        logging.StreamHandler()  # Show logs in the console
    ]
)

class ConnectionManager:
    def __init__(self, host, port=80, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.connect()
    
    def connect(self):
        logging.info(f"Connecting to {self.host}:{self.port}")
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            logging.info("Connection established successfully.")
        except Exception as e:
            logging.error(f"Failed to connect: {e}")
            raise
    
    def send_request(self, request_data):
        logging.info(f"Sending request:\n{request_data}")
        try:
            self.socket.sendall(request_data.encode())
            response_data = b""
            while True:
                chunk = self.socket.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            logging.info("Response received.")
            return response_data.decode()
        except Exception as e:
            logging.error(f"Error while sending request: {e}")
            raise
    
    def close(self):
        logging.info("Closing connection.")
        try:
            self.socket.close()
        except Exception as e:
            logging.error(f"Error while closing connection: {e}")

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

        logging.debug(f"Built request:\n{request_line}{header_lines}\n{body_data}")
        return f"{request_line}{header_lines}\r\n{body_data}"

class ResponseParser:
    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.headers = {}
        self.body = None
        self.status_code = None
        self.parse_response()

    def parse_response(self):
        try:
            header, _, body = self.raw_response.partition('\r\n\r\n')
            status_line, *header_lines = header.splitlines()
            self.status_code = int(status_line.split()[1])
            for line in header_lines:
                if ": " in line:
                    key, value = line.split(": ", 1)
                    self.headers[key] = value.strip()
            self.body = body
            logging.info(f"Response parsed: Status code {self.status_code}")
        except Exception as e:
            logging.error(f"Error while parsing response: {e}")
            raise

    def get_json(self):
        try:
            return json.loads(self.body)
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding failed: {e}")
            return None

class AuthManager:
    def __init__(self):
        self.auth_headers = {}

    def set_basic_auth(self, username, password):
        auth_str = f"{username}:{password}".encode("utf-8")
        auth_header = "Basic " + base64.b64encode(auth_str).decode("utf-8").strip()
        self.auth_headers["Authorization"] = auth_header
        logging.info("Basic authentication headers set.")
    
    def set_bearer_token(self, token):
        self.auth_headers["Authorization"] = f"Bearer {token}"
        logging.info("Bearer token set.")

class HTTPClient:
    def __init__(self, host, port=80):
        self.host = host
        self.port = port
        self.connection = ConnectionManager(host, port)
        self.auth_manager = AuthManager()
        self.history = []

    def request(self, method, path, headers=None, params=None, body=None):
        headers = headers or {}
        headers.update(self.auth_manager.auth_headers)

        request = RequestBuilder(method, path, headers=headers, params=params, body=body)
        request_data = request.build_request()

        try:
            raw_response = self.connection.send_request(request_data)
            response = ResponseParser(raw_response)
            self.history.append((request_data, response))
            logging.info(f"Request completed: {method} {path} -> {response.status_code}")
            return response
        except Exception as e:
            logging.error(f"Request failed: {method} {path} -> {e}")
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

    def view_history(self):
        for idx, (req, resp) in enumerate(self.history):
            logging.info(f"Request {idx + 1}:\n{req}\nResponse:\n{resp.raw_response}\n")

