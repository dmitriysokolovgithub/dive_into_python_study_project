import socket
import time
import traceback
import re


class ClientError(Exception):
    def __init__(self, message=None):
        if message is None:
            self.message = "bad response from server"
        else:
            self.message = message
        super().__init__(message)


class Client:
    def __init__(self, host, port, timeout=None):
        if timeout is None:
            self.socket = socket.create_connection((host, port))
        else:
            self.socket = socket.create_connection((host, port), timeout)

    def put(self, server_name, value, timestamp=None):
        try:
            if timestamp is None:
                timestamp = int(time.time())
            if type(server_name) != str or (type(value) != int and type(value) != float) and type(timestamp) != int:
                raise ClientError("put: incorrect arguments")
            put_command = f"put {str(server_name)} {str(value)} {str(timestamp)}\n"
            put_command_bytes = put_command.encode('utf-8')
            self.socket.sendall(put_command_bytes)
            response_bytes = self.socket.recv(4096)
            response = response_bytes.decode('utf-8')
            print(f'response = {response}')
            if "error" in response:
                raise ClientError("put: incorrect response from server")
        except ClientError:
            raise
        except Exception:
            raise ClientError("put: unknown error")

    def get(self, metric):
        try:
            get_command = f"get {str(metric)}\n"
            get_command_bytes = get_command.encode('utf-8')
            self.socket.sendall(get_command_bytes)
            response_bytes = self.socket.recv(4096)
            response = response_bytes.decode('utf-8')
            print(f'response = {response}')
            result = {}
            search_good_response = re.search(r'^(ok\n(\S+\s-?[\d\.]+\s\d+\n)*\n)$', response)
            if not bool(search_good_response):
                raise ClientError("get: incorrect response from server")
            if response == "ok\n\n":
                return result
            response_all_params_in_one_text = response.replace('ok\n', '')
            response_all_params_collection = response_all_params_in_one_text.split('\n')

            for params in response_all_params_collection:
                if not params:
                    continue
                param_name, param_value, param_timestamp = params.split(' ')
                new_value = (int(param_timestamp), float(param_value))
                if param_name in result:
                    result[param_name].append(new_value)
                    result[param_name].sort(key=lambda x: x[0])  # order by 1st value in tuple
                else:
                    result[param_name] = [new_value]
            return result
        except ClientError:
            raise
        except Exception:
            error_message = f"get: unknown error: {traceback.format_exc()}"
            raise ClientError(error_message)
