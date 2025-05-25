# 🕵️‍♂️ Projeto C2 - Servidor de Comando e Controle

Este repositório contém um sistema simples de C2 (Comando e Controle), composto por três componentes principais escritos em Python:

- 🖥️ `servidor/`: Servidor C2 que gerencia conexões dos agentes e do admin
- 🐍 `agente/`: Código que representa o cliente/implant (agente remoto)
- 🧑‍💼 `admin/`: Interface de controle para o operador C2

> ⚠️ **ATENÇÃO:** Este projeto é destinado exclusivamente para fins educacionais, acadêmicos e de testes em ambientes controlados. **O uso não autorizado ou malicioso deste código pode ser ilegal.** Utilize com responsabilidade e sempre com permissão explícita.

---

## 📂 Estrutura do Projeto

```bash
gc25/
├── servidor/
│   ├── command.py          # Classe Command que gerencia agentes e comandos
│   ├── agent.py            # Classe Agent que representa os agentes conectados
│   └── main.py             # Servidor principal que gerencia conexões dos agentes
├── clientes/
│   └── agente.py           # Código que conecta ao servidor, executa comandos e retorna saídas
├── admin/
│   └── admin.py            # Ferramenta para o operador enviar comandos e visualizar respostas
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```
## Documentação

#### Comandos admin

| Comandos   | Exemplo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `ls` | `ls` | Retorna o panorama atual da conexão de todos os Agents |
| `exit` | `exit` | Finaliza a interface de gerenciamento do Admin |
| `session [0-9] > comando` | `s1>whoami` | Define o comando a ser executado pelo Agent a partir do número da sessão
| `broadcast > comando` | `b>ipconfig` | Envia um comando para todos Agents que possuem sessão atualmente no Servidor |
| `default > comando` | `d>hostname` | Define o comando inicial para os novos Agents que ingressarem |

## Funcionalidades

- Autoreconexão
- Sistema de autenticação simples
- Comunicação via HTTP
