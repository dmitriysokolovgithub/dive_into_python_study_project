"""
This is an auxiliary script for testing the server.

First, start your server at 127.0.0.1 and port 8888, and then
run this script.
"""
import sys
from client.client import Client, ClientError


def run(host, port):
    client1 = Client(host, port, timeout=5)
    client2 = Client(host, port, timeout=5)
    command = "wrong command test\n"
    data_1 = None
    data_2 = None
    try:
        data = client1.get(command)
    except ClientError:
        pass
    except BaseException as err:
        print(f"Server connection error: {err.__class__}: {err}")
        sys.exit(1)
    else:
        print("An invalid command sent to the server should return a protocol error")
        sys.exit(1)

    command = 'some_key'
    try:
        data_1 = client1.get(command)
        data_2 = client1.get(command)
    except ClientError:
        print('The server returned a response to a valid request, '
              'which the client determined to be invalid.. ')
    except BaseException as err:
        print(f"The server returned a response to a valid request, "
              f"which the client determined to be invalid: {err.__class__}: {err}")
        sys.exit(1)

    assert data_1 == data_2 == {}, \
        "When a client requests a data from a non-existent key, " \
        "the server must return a response with an empty data field."

    try:
        data_1 = client1.get(command)
        data_2 = client2.get(command)
    except ClientError:
        print('The server returned a response to a valid request, '
              'which the client determined to be invalid.. ')
    except BaseException as err:
        print(f"The server must be able to connect to multiple clients: "
              f"{err.__class__}: {err}")
        sys.exit(1)

    assert data_1 == data_2 == {}, \
        "When a client requests a data from a non-existent key, " \
        "the server must return a response with an empty data field."

    try:
        client1.put("k1", 0.25, timestamp=1)
        client2.put("k1", 2.156, timestamp=2)
        client1.put("k1", 0.35, timestamp=3)
        client2.put("k2", 30, timestamp=4)
        client1.put("k2", 40, timestamp=5)
        client1.put("k2", 41, timestamp=5)
    except Exception as err:
        print(f"Call error 'client.put(...)' {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {
        "k1": [(1, 0.25), (2, 2.156), (3, 0.35)],
        "k2": [(4, 30.0), (5, 41.0)],
    }

    try:
        metrics = client1.get("*")
        if metrics != expected_metrics:
            print(f"client.get('*') returned incorrect result. Expected: "
                  f"{expected_metrics}. Received: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Call error client.get('*') {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {"k2": [(4, 30.0), (5, 41.0)]}

    try:
        metrics = client2.get("k2")
        if metrics != expected_metrics:
            print(f"client.get('k2') returned incorrect result. Expected: "
                  f"{expected_metrics}. Received: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Call error 'client.get('k2')' {err.__class__}: {err}")
        sys.exit(1)

    try:
        result = client1.get("k3")
        if result != {}:
            print(
                f"Error calling the get method with a key that has not yet been added."
                f"Expected: empty dictionary. Received: {result}")
            sys.exit(1)
    except Exception as err:
        print(f"Error calling the get method with a key that has not yet been added: "
              f"{err.__class__} {err}")
        sys.exit(1)

    print("All right!")


if __name__ == "__main__":
    run("127.0.0.1", 8181)
