# Solicitar ao usuário para digitar um número
numero = int(input("Digite um número: "))

# Solicitar ao usuário para escolher uma ação
acao = int(input('''\nEscolha uma das opções:
1. Transcrever o número para binário
2. Transcrever o número para hexadecimal
3. Transcrever o número para octal
4. Não fazer nada
Digite a ação que deseja realizar: '''))

# Verificar qual ação o usuário deseja realizar
if acao == 1:
    print(f"O número {numero} em binário é {bin(numero)[2:]}")
elif acao == 2:
    print(f"O número {numero} em hexadecimal é {hex(numero)[2:]}")
elif acao == 3:
    print(f"O número {numero} em octal é {oct(numero)[2:]}")
elif acao == 4:
    print("Nenhuma ação foi realizada")
    print(f"O número digitado foi: {numero}")
    print("Fim do programa")
else:
    print("Opção inválida! Por favor, reinicie o programa e escolha uma opção de 1 a 4.")
