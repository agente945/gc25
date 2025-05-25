import uuid
from datetime import datetime


class Agent:

    _default_command = "whoami"

    @classmethod
    def set_default_command(cls, command):
        cls._default_command = command

    @classmethod
    def _get_default_command(cls):
        return cls._default_command

    def __init__(self, ip):
        self._token = str(uuid.uuid4())
        self._ip = ip
        self._lastCommunication = datetime.now()

        self._nextCommand = self._get_default_command()
        self._lastResponse = ""
        self._lastCommand = ""

    def update_last_communication(self):
        self.last_communication = datetime.now()

    def command_request(self):
        if self.next_command:
            self.update_last_communication()
            self.last_command = self.next_command
            self.next_command = ""
            return self.last_command
        return self._nextCommand

    # Getters
    @property
    def token(self):
        return self._token

    @property
    def ip(self):
        return self._ip

    @property
    def last_communication(self):
        return self._lastCommunication

    @property
    def next_command(self):
        return self._nextCommand

    @property
    def last_response(self):
        return self._lastResponse

    @property
    def last_command(self):
        return self._lastCommand

    # Setters
    @last_response.setter
    def last_response(self, response):
        self.update_last_communication()
        self._lastResponse = response

    @next_command.setter
    def next_command(self, command):
        self._nextCommand = command

    @last_command.setter
    def last_command(self, command):
        self._lastCommand = command

    @last_communication.setter
    def last_communication(self, value):
        self._lastCommunication = value
