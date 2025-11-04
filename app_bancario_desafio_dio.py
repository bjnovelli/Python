from abc import ABC, abstractmethod
from datetime import datetime

# ------------------ CLASSES DE CLIENTES ------------------

class Cliente:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, endereco, data_nascimento):
        super().__init__(nome, endereco)
        self.cpf = cpf
        self.data_nascimento = data_nascimento


# ------------------ CLASSE HISTÓRICO ------------------

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

    @property
    def extrato(self):
        return self.transacoes


# ------------------ CLASSE CONTA ------------------

class Conta:
    def __init__(self, numero, cliente):
        self.numero = numero
        self._agencia = "0001"
        self.cliente = cliente
        self._saldo = 0
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def agencia(self):
        return self._agencia

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor

    def sacar(self, valor):
        if valor <= 0:
            print("Valor inválido para saque.")
            return False
        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False

        self._saldo -= valor
        print(f"Saque de R${valor:.2f} realizado com sucesso.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido para depósito.")
            return False

        self._saldo += valor
        print(f"Depósito de R${valor:.2f} realizado com sucesso.")
        return True


# ------------------ CONTA CORRENTE ------------------

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([t for t in self.historico.transacoes if t["tipo"] == "Saque"])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou! Você excedeu o limite de saque.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"Conta Corrente Nº {self.numero} | Cliente: {self.cliente.nome} | Saldo: R${self.saldo:.2f}"


# ------------------ CLASSES DE TRANSAÇÃO ------------------

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# ------------------ PROGRAMA PRINCIPAL ------------------

if __name__ == "__main__":
    cliente = PessoaFisica("123.456.789-00", "João Silva", "Rua A, 123", "01/01/1990")
    conta = ContaCorrente.nova_conta(cliente, 1)

    deposito = Deposito(1000)
    deposito.registrar(conta)

    saque1 = Saque(200)
    saque1.registrar(conta)

    saque2 = Saque(400)
    saque2.registrar(conta)

    print("\n--- EXTRATO ---")
    for t in conta.historico.extrato:
        print(f"{t['data']} | {t['tipo']} | R${t['valor']:.2f}")

    print("\n", conta)
