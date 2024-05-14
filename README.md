# Metric Collection System

This project involves developing a system for collecting and storing various numerical metrics using a client-server architecture. This is the final project for the "Dive into Python" [course on Coursera](https://www.coursera.org/account/accomplishments/certificate/PJMZJMEZMV92).

![Project scheme](/documentation/scheme.jpg)

## Client Implementation

### Description

In large-scale projects with many users, it is crucial to monitor all ongoing processes. These processes can be represented by various numerical metrics such as the number of requests to your application, response times, daily user counts, and more.

### Interaction Protocol

- The client and server communicate via a simple text protocol over TCP sockets.
- The protocol supports two types of requests from the client to the server:
  - Sending data to be saved on the server (`put` command)
  - Retrieving saved data from the server (`get` command)

### General Request and Response Formats

- Client request format:
`<command> <request data>\n`
- Server response format:
`<status>\n<response data>\n\n`

### Client Implementation

Implement a `Client` class encapsulating the connection to the server, client socket, and methods for sending (`put`) and receiving (`get`) metrics.

#### Constructor Parameters

- `host`: Server host address.
- `port`: Server port.
- `timeout`: Optional timeout value (default is `None`).

#### Methods

- `put(metric, value, timestamp=None)`: Sends data to the server.
- Parameters:
  - `metric` (string): The name of the metric.
  - `value` (float): The value of the metric.
  - `timestamp` (int, optional): The timestamp of the metric. Uses `int(time.time())` if not provided.
- Raises `ClientError` on failure.
- `get(metric)`: Retrieves data from the server.
- Parameter:
  - `metric` (string): The name of the metric. Use `*` to retrieve all metrics.
- Returns a dictionary with metrics.
- Raises `ClientError` on failure.

#### Example Usage

from solution import Client

client = Client("127.0.0.1", 8888, timeout=15)
client.put("palm.cpu", 0.5, timestamp=1150864247)
data = client.get("palm.cpu")

## Server Implementation

The server should handle put and get commands, parse them, and respond according to the protocol. It should save metrics in memory structures and maintain session connections between requests.

#### Example Usage

$ telnet 127.0.0.1 8888
get test_key
ok

got test_key
error
wrong command


## Environment creation and run
Run in project root directory `python -m venv env` to environment create

For env run: `env\Scripts\activate`

For deactivate: `env\Scripts\deactivate` or close terminal

## Requirements
Python version: v.3.6

`pip install -r requirements.txt`

## Test run
Run in project root directory

Run server from the first terminal: `python server\server.py`

Run client comands script from the second terminal: `python main.py`
