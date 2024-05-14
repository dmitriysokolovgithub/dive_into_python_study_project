import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import pytest
from client.client import ClientError
import time


class TestPut:
    @pytest.mark.parametrize('server_name', ["palm.cpu", "second", "2132", "seco3232nd"])
    def test_put_correct_different_servers(self, client, server_name):
        client.put(server_name, 23.7, 1150864247)

    @pytest.mark.parametrize('arg_value', [23.7, 323, -12, 0, 434343.23])
    def test_put_correct_different_values(self, client, arg_value):
        client.put("palm.cpu", arg_value, 1150864247)

    @pytest.mark.parametrize('arg_timestamp', [1150864247, None])
    def test_put_correct_different_timestamp(self, client, arg_timestamp):
        client.put("palm.cpu", 23.7, arg_timestamp)

    @pytest.mark.parametrize('server_name', ['\n', None])
    def test_put_incorrect_different_servers(self, client, server_name):
        try:
            client.put(server_name, 23.7, 1150864247)
            assert False, "Expected client error"
        except ClientError:
            assert True

    @pytest.mark.parametrize('arg_value', ["323ds", "", None, "ddsf"])
    def test_put_incorrect_different_values(self, client, arg_value):
        try:
            client.put("palm.cpu", arg_value, 1150864247)
            assert False, "Expected client error"
        except ClientError:
            assert True

    @pytest.mark.parametrize('arg_timestamp', ["sfdsf", "dsdd32", 323.32])
    def test_put_incorrect_different_timestamp(self, client, arg_timestamp):
        try:
            client.put("palm.cpu", 23.7, arg_timestamp)
            assert False, "Expected client error"
        except ClientError:
            assert True

    def test_get_one_server_should_correct(self, client):
        timestamp_value = int(time.time())
        time.sleep(1)
        server_name = f"palma.cpu_{str(timestamp_value)}"
        metric_value = 5.0
        client.put(server_name, metric_value, timestamp_value)
        correct_value = [(timestamp_value, metric_value)]
        output = client.get(server_name)
        if server_name in output and output[server_name] == correct_value:
            assert True
        else:
            assert False, f"Incorrect 'get' response: '{str(output[server_name])}', '{str(correct_value)}'"

    def test_get_several_servers_should_correct(self, client):
        timestamp_value = int(time.time())
        first_server_name = f"palma.cpu_{str(timestamp_value)}"
        metric_value = 5.0
        client.put(first_server_name, metric_value, timestamp_value)
        first_correct_value = [(timestamp_value, metric_value)]
        time.sleep(1)
        timestamp_value = int(time.time())
        second_server_name = f"palma.cpu_{str(timestamp_value)}"
        metric_value = 5.0
        client.put(second_server_name, metric_value, timestamp_value)
        second_correct_value = [(timestamp_value, metric_value)]
        output = client.get("*")
        if first_server_name in output and output[first_server_name] == first_correct_value\
                and second_server_name in output and output[second_server_name] == second_correct_value:
            assert True
        else:
            assert False, f"Incorrect 'get' response"
