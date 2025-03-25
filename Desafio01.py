'''
Implementar um sistema bancário 
que conta com as operações:
- depósito: depósitos positivos e devem ser armazenados 
em uma variável e exibidos na operação extrato.
- saque: permite 3 saques com no máximo 500 reais por 
saque. Se não tem saldo, exibir mensagem. Saques devem 
ser armazenados e registrados no extrato 
- extrato: listar depositos e saques da conta. 
No fim, exibir saldo atual. Exibir no formato R$xxx.xx. 
Exemplo: R$1500.45
'''
saldo = 0
registros = []
limite_saques = 3
valor_limite_saques = 500
def deposito_bancario(valor: float):
    global saldo
    if valor >= 0:
        saldo += valor
        registros.append(f"Depósito: + R$ {valor:.2f}")
        print(f"Depósito no valor de R$ {valor:.2f} realizado com sucesso!")
    elif valor < 0:
        print("Valor inválido para depósito! Tente valores positivos")
    print()

def saque_bancario(valor: float):
    global saldo, limite_saques
    
    if limite_saques <= 0:
        print("Erro: você já atingiu o limite de 3 saques diários!")

    if valor > saldo:
        print("Saldo insulficiente para saque! Faça depósitos para conseguir sacar em uma próxima tentativa.")
    
    elif valor < 0:
        print("Tentativa com valores negativos não são permitidas. Tente outro valor!")
    elif valor > valor_limite_saques:
        print(f"Valor máximo é de R$ {valor_limite_saques:.2f} reais por saque.")
    
    elif ((valor <= saldo) and (valor > 0)) and (limite_saques > 0):
        saldo -= valor
        limite_saques -= 1
        registros.append(f"Saque: - R$ {valor:.2f}")
        print(f"Saque no valor de R$ {valor:.2f} realizado com sucesso!")
    
    else:
        print("Tente outra opção!")


def extrato_bancario():
    print("\n=============== EXTRATO ==================")
    if not registros:
        print("Não há registros de movimentação bancária")
    else:
        for movimentacao in registros:
            print(movimentacao)
    print(f"\n SALDO: R$ {saldo:.2f}")
    print("==========================================")
     

mensagem = f'''
            ########### MENU ############
        
            [1] Depositar
            [2] Sacar
            [3] Extrato
            [0] Sair
        
            ##############################
'''

while True:
    print(mensagem)

    opcao = int(input("Olá! Como posso te ajudar hoje? Escolha uma opção.\n=>"))

    if opcao == 1:
        depositar_valor = float(input("Informe o valor do depósito: "))
        deposito_bancario(depositar_valor)

    elif opcao == 2:
        sacar_valor = float(input("Informe um valor para saque: "))
        saque_bancario(sacar_valor)

    elif opcao == 3:
        extrato_bancario()
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
    

#sacar = saque_bancario
#exibir_extrato = extrato_bancario100