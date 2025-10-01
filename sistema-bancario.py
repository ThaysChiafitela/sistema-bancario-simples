import datetime

def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def registrar_transacao(tipo, valor, extrato):
    return {
        "tipo": tipo,
        "valor": valor,
        "data_hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "extrato": extrato
    }

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        transacao = registrar_transacao("Depósito", valor, extrato)
        extrato.append(transacao)
        print(f"\nDepósito de {formatar_valor(valor)} realizado com sucesso!")
    else:
        print("\n## Operação falhou! O valor informado é inválido. ##")
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n## Operação falhou! Você não tem saldo suficiente. ###")

    elif excedeu_limite:
        print("\n## Operação falhou! O valor do saque excede o limite de R$ 500,00. ##")

    elif excedeu_saques:
        print("\n## Operação falhou! Número máximo de saques diários (3) excedido. ##")

    elif valor > 0:
        saldo -= valor
        transacao = registrar_transacao("Saque", valor, extrato)
        extrato.append(transacao)
        numero_saques += 1
        print(f"\nSaque de {formatar_valor(valor)} realizado com sucesso!")

    else:
        print("\n## Operação falhou! O valor informado é inválido. ##")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO BANCÁRIO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in extrato:
            tipo = transacao["tipo"]
            valor = transacao["valor"]
            data_hora = transacao["data_hora"]
            print(f"[{data_hora}] {tipo}: {formatar_valor(valor)}")

    print(f"\nSaldo Atual: {formatar_valor(saldo)}")
    print("==================================================")

def main():
    menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

    # Variáveis de estado
    saldo = 0
    limite = 500
    extrato = [] # Lista de dicionários para armazenar as transações
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = input(menu).lower().strip()

        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: "))
            except ValueError:
                print("\n## Entrada inválida. Por favor, digite um número. ##")
                continue
            
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: "))
            except ValueError:
                print("\n## Entrada inválida. Por favor, digite um número. ##")
                continue
            
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "q":
            print("\nObrigado por utilizar nosso sistema bancário. Até mais!")
            break

        else:
            print("\n## Operação inválida, por favor selecione novamente a operação desejada. ##")

if __name__ == "__main__":
    main()