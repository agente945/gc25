import http.client
import re
import threading
import time
from time import sleep

host = "127.0.0.1:80"  # Mude isso
token = ""
parar_loop_de_logs = False
am_i_online = False


def reinicia():
    global token, parar_loop_de_logs, am_i_online

    parar_loop_de_logs = True
    am_i_online = False
    token = ""


def comunica(data):
    global token

    try:
        conn = http.client.HTTPConnection(host)

        conn.request("POST", "/", data.encode(), headers={"token": token})
        response = conn.getresponse()
        body = response.read().decode()
        if response.status != 200 or body == "False":
            reinicia()
        return body
    except:
        reinicia()
        return ""


def check_update():
    resposta = comunica("ping")
    inicio_msg = "pong|"

    if not resposta.startswith(inicio_msg):
        reinicia()
        # print("Verifique o token")
        return False

    if len(resposta) > len(inicio_msg):
        print(resposta[len(inicio_msg) :])

    return True


def loop_de_logs():
    global token, parar_loop_de_logs

    parar_loop_de_logs = False

    while not parar_loop_de_logs:
        # print("Tem notificacao?")
        check_update()
        time.sleep(2)


def loop_de_comandos():
    global parar_loop_de_logs

    while am_i_online:
        cmd = input("")  # bloqueia apenas esta thread
        if cmd.lower() in ("sair", "exit", "quit", "end"):
            print("Encerrando…")
            parar_loop_de_logs = True
            break

        elif cmd.lower() == "ls":
            comunica("ls")
            continue

        elif re.match(r"(?:s|session) ?(\d+) ?> ?(.*)", cmd, re.IGNORECASE):
            comunica(cmd)

        elif re.match(r"(?:b|broadcast|d|default) ?> ?(.*)", cmd, re.IGNORECASE):
            comunica(cmd)

        else:
            print(f"Command not found.'{cmd}'")

    parar_loop_de_logs = False


if __name__ == "__main__":
    while True:

        sleep(1)

        if not re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}$",
            token,
        ):
            token = input("Token de acesso:")
            am_i_online = False
            continue

        if not check_update():
            print("Reconectando.")
            am_i_online = False
            continue

        if not am_i_online:
            print("Conectado.")
            am_i_online = True

        # Cria e inicia a thread de logging
        t_log = threading.Thread(target=loop_de_comandos, daemon=True)
        t_log.start()

        # Loop principal de comandos (bloqueante)
        loop_de_logs()
