import cloudpickle
import requests
import ipaddress
import socket
from utils.exception import InvalidServerAddressError, InvalidPortError


class PandaTask:
    def __init__(self, func, server_address, server_port):
        self.func = func
        self.server_address = server_address
        self.server_port = server_port

        if not self.validate_server_address():
            raise InvalidServerAddressError("Invalid server address.")

        if not self.validate_port():
            raise InvalidPortError("Invalid port number.")

    def serialize_function(self):
        serialized_func = cloudpickle.dumps(self.func)
        return serialized_func

    def upload_code(self, timeout=10, max_retries=3):
        url = f"http://{self.server_address}:{self.server_port}/upload"
        serialized_func = self.serialize_function()

        for retry in range(1, max_retries+1):
            try:
                response = requests.post(url, data=serialized_func, timeout=timeout)
                if response.status_code == 200:
                    print("Upload successful.")
                    return
                else:
                    print("Failed to upload serialized code.")
            except requests.exceptions.RequestException as e:
                print(f"Upload timeout, retrying ({retry}/{max_retries})...")
                continue

        print("Upload failed. Please check and retry.")

    def validate_server_address(self):
        try:
            ipaddress.ip_address(self.server_address)
            return True
        except ValueError:
            try:
                socket.gethostbyname(self.server_address)
                return True
            except socket.gaierror:
                return False

    def validate_port(self):
        try:
            port = int(self.server_port)
            return 0 <= port <= 65535
        except ValueError:
            return False
