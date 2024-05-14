import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import pytest
from client.client import Client


@pytest.fixture(autouse=True, scope="class")
def client():
    host = "127.0.0.1"
    port = 10001
    client = Client(host, port)
    return client
