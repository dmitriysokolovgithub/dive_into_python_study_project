import re
import asyncio
from random import randint
from copy import deepcopy


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()


class Storage:
    def __init__(self):
        self._params = {}

    def get(self, key):
        if key == '*':
            return deepcopy(self._params)

        if key in self._params:
            return deepcopy(self._params[key])

        return {}

    def update(self, server_name, server_timestamp, metric_value):
        adding_value = (server_timestamp, metric_value)
        # parameter is already exists
        if server_name in self._params and not adding_value in self._params[server_name]:
            # searching for a value with the same timestamp
            for i, (existing_timestamp, existing_value) in enumerate(self._params[server_name]):
                # value with the same timestamp is already exists
                if existing_timestamp == server_timestamp:
                    # replace existing value-tuple with the new value-tuple
                    self._params[server_name][i] = adding_value
                    return
            # no matches
            self._params[server_name].append(adding_value)
            print(f"add existing key = '{server_name}'")
        else:
            self._params[server_name] = [adding_value]
            print(f"add new key = '{server_name}'")


class ClientServerProtocol(asyncio.Protocol):
    machines_params = Storage()

    def __init__(self):
        self.transport = None

    def process_data(self, decoded_data):
        """
        The method checks the input command from the client and returns a response based on the input command
        :param decoded_data: the input command from the client
        :return: response from server
        """
        session = str(randint(0, 32000))
        response_command = 'error\nwrong command\n\n'
        if decoded_data and len(decoded_data) > 3:
            print(f"{session}: decoded_data = {decoded_data}")
            input_command = decoded_data[:3]
            if input_command == "put":
                print(f"{session}: PUT")
                check_input = re.search(r'^(put\s(\S+)+\s(-?[0-9]+[.]?[0-9]*)\s(\d+)\n)$', decoded_data)
                if bool(check_input) and len(check_input.groups()) == 4:
                    response_command = 'ok\n\n'
                    all_input, in_server_name, in_metric_value, in_server_timestamp = check_input.groups()
                    ClientServerProtocol.machines_params.update(in_server_name, int(in_server_timestamp),
                                                       float(in_metric_value))
                    print(f"{session}: machines_params = '{str(ClientServerProtocol.machines_params)}'")
            elif input_command == "get":
                print(f"{session}: GET")
                check_input = re.search(r'^(get\s(\S+)\n)$', decoded_data)
                if bool(check_input) and len(check_input.groups()) == 2:
                    rough_response_command = 'ok\n'
                    in_server_name = check_input.groups()[1].replace("\n", "")
                    print(f"{session}: input_server_name = '{in_server_name}'")
                    if in_server_name == '*':
                        print(f"{session}: IF")
                        for out_server_name in ClientServerProtocol.machines_params.get("*"):
                            for out_pair_value in ClientServerProtocol.machines_params.get(out_server_name):
                                out_server_timestamp, out_metric_value = out_pair_value
                                rough_response_command += \
                                    f'{out_server_name} {str(out_metric_value)} {str(out_server_timestamp)}\n'
                        rough_response_command += '\n'
                        response_command = rough_response_command
                    elif in_server_name in ClientServerProtocol.machines_params.get("*"):
                        print(f"{session}: ELIF")
                        for out_pair_value in ClientServerProtocol.machines_params.get(in_server_name):
                            out_server_timestamp, out_metric_value = out_pair_value
                            rough_response_command += \
                                f'{in_server_name} {str(out_metric_value)} {str(out_server_timestamp)}\n'
                        rough_response_command += '\n'
                        response_command = rough_response_command
                    else:
                        print(f"{session}: ELSE")
                        print(f"{session}: machines_params keys = "
                              f"{str(', '.join(ClientServerProtocol.machines_params.get('*').keys()))}")
                        response_command = 'ok\n\n'
                else:
                    print(f"{session}: ELSE!!!")
        else:
            print(f"{session}: NOT GET AND NOT PUT!!!")
        print(f"{session}: server command = '{response_command}'")
        return response_command

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        """
        The method is automatically called by the asyncio framework when it receives data from the client
        :param data: binary data from client
        :return: None
        """
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())


if __name__ == '__main__':
    host, port = '127.0.0.1', 8181
    run_server(host, port)
