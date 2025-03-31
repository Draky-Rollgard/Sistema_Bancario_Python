''''''''''''''''''''''''''''''''''''
import textwrap

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

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")

    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("Erro: CPF já cadastrado.")
        return None

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    usuarios.append({
        "nome": nome, 
        "data_nascimento": data_nascimento, 
        "cpf": cpf, "endereco": endereco,
    })
    print(f"Usuário {nome} criado com sucesso!")


def criar_conta_corrente(agencia, usuarios, contas):
    cpf = input("Informe o CPF do usuário para vincular a conta: ")
    usuario = next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)
    if usuario:
        conta = {
            "agencia": agencia, 
            "numero_conta": len(contas) + 1, 
            "usuario": usuario
        }
        contas.append(conta)
        print("\nConta criada com sucesso!")
    else:
        print("\nUsuário não encontrado!")

def deposito_bancario(saldo, valor, registros, /):
    if valor >= 0:
        saldo += valor
        registros.append(f"Depósito: + R$ {valor:.2f}")
        print(f"Depósito no valor de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Valor inválido para depósito! Tente valores positivos.")
    return saldo, registros

def saque_bancario(*, saldo, valor, registros, valor_limite_saques, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print("Erro: você já atingiu o limite de 3 saques diários!")
        return saldo, registros, numero_saques

    elif valor > saldo:
        print("Saldo insuficiente para saque! Faça depósitos para conseguir sacar em uma próxima tentativa.")
        return saldo, registros, numero_saques
    
    elif valor < 0:
        print("Tentativa com valores negativos não são permitidas. Tente outro valor!")
        return saldo, registros, numero_saques
    
    elif valor > valor_limite_saques:
        print(f"Valor máximo é de R$ {valor_limite_saques:.2f} reais por saque.")
        return saldo, registros, numero_saques
    
    elif ((valor <= saldo) and (valor > 0)) and (limite_saques > 0):
        saldo -= valor
        numero_saques += 1
        registros.append(f"Saque: - R$ {valor:.2f}")
        print(f"Saque no valor de R$ {valor:.2f} realizado com sucesso!")
        return saldo, registros, numero_saques

    else:
        print("Tente outra opção!")


def extrato_bancario(registros, /, *, saldo):
    print("\n=============== EXTRATO ==================")
    if not registros:
        print("Não há registros de movimentação bancária")
    else:
        for movimentacao in registros:
            print(movimentacao)
    print(f"\n SALDO: R$ {saldo:.2f}")
    print("==========================================")

def listar_contas(contas):
    if not contas:
        print("Não há contas cadastradas.")
    else:
        for conta in contas:
            print("=====================================================")
            print(f"Agência:\t{conta['agencia']}\nC/C:\t{conta['numero_conta']}\nTitular:\t{conta['usuario']['nome']}")
            print("=====================================================")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    saldo = 0
    valor_limite_saques = 500
    numero_saques = 0    
    
    registros = []
    usuarios = []
    contas = []

    while True:
        try:
            opcao = int(menu())  
        except ValueError:
            print("Erro: Digite um número válido.")
            continue
        
        if opcao == 1:
            depositar_valor = float(input("Informe o valor do depósito: "))

            saldo, registros = deposito_bancario(saldo, depositar_valor, registros)

        elif opcao == 2:
            sacar_valor = float(input("Informe um valor para saque: "))

            saldo, registros, numero_saques = saque_bancario(
                saldo=saldo, 
                valor=sacar_valor, 
                registros=registros, 
                valor_limite_saques=valor_limite_saques, 
                numero_saques= numero_saques, 
                limite_saques=LIMITE_SAQUES,
                )

        elif opcao == 3:
            extrato_bancario(registros, saldo=saldo)

        elif opcao == 4:
            listar_contas(contas)

        elif opcao == 5:
            criar_usuario(usuarios)

        elif opcao == 6:
            criar_conta_corrente(AGENCIA, usuarios, contas)

        elif opcao == 0:
            print(''' 
            Obrigado por fazer uso do nosso sistema! 
            Operações do dia finalizadas. 
            (^-^) Até logo! 
            ''')
            break

        else:
            print("Tente uma opção válida.")
            continue
main()