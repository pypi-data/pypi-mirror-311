import json
import logging
from ctypes import Union
from json import JSONDecodeError

from websockets.sync.client import connect


class WebsocketClient:
    """
    A client for connecting to a WebSocket server and sending/receiving messages.
    """

    def __init__(self, server: str, log=logging):
        """
        Initializes a WebsocketClient instance.

        :param server: The WebSocket server address.
        :param log: The logging instance to use for logging errors.
        """
        self._server = self._parse_server(server)
        self._log = log

    def send(self, channel: str, message, headers=None, timeout=None):
        """
        Sends a message to a specified channel on the WebSocket server.

        :param channel: The channel to send the message to.
        :param message: The message to be sent.
        :param headers: Optional headers to include in the WebSocket connection.
        """
        connection = f"wss://{self._server}?channel={channel}"
        headers = headers if headers else {}
        with connect(connection, additional_headers=headers, open_timeout=timeout) as websocket:
            websocket.send(json.dumps(message, default=str))
            websocket.close()

    def wait_message(self, channel, timeout=30, headers=None):
        """
        Waits for a message from a specified channel on the WebSocket server.

        :param channel: The channel to listen for messages.
        :param timeout: The time in seconds to wait for a message before timing out.
        :param headers: Optional headers to include in the WebSocket connection.
        :return: The received message, or None if an error occurs or timeout is reached.
        """
        connection = f"wss://{self._server}?channel={channel}"
        headers = headers if headers else {}
        with connect(connection, additional_headers=headers) as websocket:
            try:
                message = websocket.recv(timeout=timeout)
                try:
                    message = json.loads(message)
                except JSONDecodeError:
                    pass  # If message is not valid JSON, return as is
            except TimeoutError:
                message = None  # Return None if the operation times out
            except Exception as e:
                self._log.error(str(e))  # Log any other exceptions
                message = None
            return message

    def _parse_server(self, server):
        """
        Parses the server address to extract the server name.

        :param server: The server address.
        :return: The parsed server name.
        """
        return server.split(":")[-1]
