import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao("Depósito", self.valor)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta):
        if self.valor > conta.saldo:
            print("Saldo insuficiente!")
        elif conta.saques_realizados >= conta.limite_saques:
            print("Limite de saques atingido!")
        elif self.valor > conta.limite:
            print("Valor do saque excede o limite!")
        else:
            conta.saldo -= self.valor
            conta.saques_realizados += 1
            conta.historico.adicionar_transacao("Saque", self.valor)

class Historico:
    def __init__(self):
        self.transacoes = []
    
    def adicionar_transacao(self, tipo, valor):
        self.transacoes.append({"tipo": tipo, "valor": valor, "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")})
    
    def exibir_extrato(self, saldo):
        print("\n=============== EXTRATO ==================")
        if not self.transacoes:
            print("Não há registros de movimentação bancária")
        else:
            for transacao in self.transacoes:
                print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
        print(f"\nSaldo atual: R$ {saldo:.2f}")
        print("==========================================")

class Conta:
    def __init__(self, cliente, numero, agencia, limite=500, limite_saques=3):
        self._saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()
        self.saques_realizados = 0
        self.limite = limite
        self.limite_saques = limite_saques
    
    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor):
        if valor >= 0:
            self._saldo = valor
    
    def sacar(self, valor):
        transacao = Saque(valor)
        transacao.registrar(self)
    
    def depositar(self, valor):
        transacao = Deposito(valor)
        transacao.registrar(self)
    
    def exibir_extrato(self):
        self.historico.exibir_extrato(self.saldo)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

def menu():
    menu = """\n
    ########### MENU ############
        
        [1]\tDepositar
        [2]\tSacar
        [3]\tExtrato
        [4]\tListar Contas
        [5]\tCriar Usuário
        [6]\tCriar Conta Corrente
        [0]\tSair
    
    ##############################
    => """
    return input(textwrap.dedent(menu))

def main():
    usuarios = []
    contas = []
    AGENCIA = "0001"
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            cpf = input("Informe o CPF do titular (somente números): ")
            valor = float(input("Informe o valor do depósito: "))
            conta = next((c for c in contas if c.cliente.cpf == cpf), None)
            if conta:
                conta.depositar(valor)
            else:
                print("Conta não encontrada!")
        
        elif opcao == "2":
            cpf = input("Informe o CPF do titular: ")
            valor = float(input("Informe o valor do saque: "))
            conta = next((c for c in contas if c.cliente.cpf == cpf), None)
            if conta:
                conta.sacar(valor)
            else:
                print("Conta não encontrada!")
        
        elif opcao == "3":
            cpf = input("Informe o CPF do titular: ")
            conta = next((c for c in contas if c.cliente.cpf == cpf), None)
            if conta:
                conta.exibir_extrato()
            else:
                print("Conta não encontrada!")
        
        elif opcao == "4":
            if not contas:
                print("Não há contas cadastradas.")
            else:
                for conta in contas:
                    print("======================================")
                    print(f"\nAgência: {conta.agencia}\nConta: {conta.numero}\nTitular: {conta.cliente.nome}")
        
        elif opcao == "5":
            cpf = input("Informe o CPF (somente números): ")
            if any(usuario.cpf == cpf for usuario in usuarios):
                print("Erro: CPF já cadastrado.")
                continue
            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereço: ")
            usuario = PessoaFisica(nome, cpf, data_nascimento, endereco)
            usuarios.append(usuario)
            print(f"Usuário {nome} criado com sucesso!")
        
        elif opcao == "6":
            cpf = input("Informe o CPF do usuário: ")
            usuario = next((u for u in usuarios if u.cpf == cpf), None)
            if usuario:
                numero_conta = len(contas) + 1
                conta = Conta(usuario, numero_conta, AGENCIA)
                usuario.adicionar_conta(conta)
                contas.append(conta)
                print("Conta criada com sucesso!")
            else:
                print("Usuário não encontrado!")
        
        elif opcao == "0":
            print('''\nObrigado por fazer uso do nosso sistema!\nOperações do dia finalizadas.\n(^-^) Até logo!\n''')
            break
        
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
