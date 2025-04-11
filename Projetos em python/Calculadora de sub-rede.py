import json  # Biblioteca para salvar os dados em formato JSON

# Função que valida se o IP está no formato correto.
def validar_ip(ip):
    partes = ip.split(".")
    if len(partes) != 4:
        return False
    for parte in partes:
        if not parte.isdigit(): # Verifica se a parte é composta apenas por numeros
            return False
        num = int(parte)
        if num < 0 or num > 255:
            return False
    return True

# Converte IP para inteiro sem bitwise
def ip_para_inteiro(ip):
    partes = ip.split(".")
    oct1 = int(partes[0])
    oct2 = int(partes[1])
    oct3 = int(partes[2])
    oct4 = int(partes[3])
    # Multiplica cada octeto pela potência correta de 256
    inteiro = (oct1 * (256**3)) + (oct2 * (256**2)) + (oct3 * 256) + oct4
    return inteiro

# Converte inteiro para IP (formato decimal pontuado)
def inteiro_para_ip(inteiro):
    oct1 = inteiro // (256**3)
    inteiro %= (256**3)

    oct2 = inteiro // (256**2)
    inteiro %= (256**2)

    oct3 = inteiro // 256
    oct4 = inteiro % 256

    return f"{oct1}.{oct2}.{oct3}.{oct4}"

# Converte um valor CIDR (ex: 24) para uma string binária com 32 bits
def mascara_para_binario(cidr):
    mascara = ""  # Inicializa uma string vazia
    for i in range(32):  # Laço que percorre de 0 até 31 (32 posições)
        if i < cidr:
            mascara += '1'  # Adiciona '1' se o índice for menor que o CIDR
        else:
            mascara += '0'  # Adiciona '0' caso contrário
    return mascara  # Retorna a máscara gerada


# Converte uma máscara binária para formato decimal
def binario_para_decimal_pontuado(binario):
    octetos = []  # Inicializa uma lista vazia para armazenar os octetos
    for i in range(0, 32, 8):  # Loop para percorrer os 32 bits em blocos de 8
        octeto_binario = binario[i:i+8]  # Pega o bloco de 8 bits
        octeto_decimal = int(octeto_binario, 2)  # Converte o bloco binário para decimal
        octetos.append(str(octeto_decimal))  # Adiciona o valor decimal à lista como string
    return ".".join(octetos)  # Junta os valores com pontos (formato de endereço IP)

# Calcula a quantidade de hosts válidos (2^bits de host - 2)
def calcular_hosts(cidr):
    # Calcula o número de bits de host
    bits_host = 32 - cidr  # O número de bits de host é 32 menos o CIDR
    numero_hosts = 2 ** bits_host  # Calcula 2 elevado ao número de bits de host
    hosts_validos = numero_hosts - 2  # Subtrai 2 para remover o endereço de rede e de broadcast
    return hosts_validos

# Converte uma máscara binária para inteiro
def binario_para_inteiro(binario):
    total = 0  # Inicializa a variável para armazenar o total
    for i in range(32):  # Loop para percorrer os 32 bits da máscara
        bit = int(binario[i])  # Converte o bit para inteiro
        peso = 2 ** (31 - i)  # Calcula o peso do bit com base na posição
        total += bit * peso  # Adiciona o valor do bit ponderado ao total
    return total

# Função principal do programa
def calculadora_sub_rede():
    endereco_ip = input("Digite o endereço IP: ")
    while not validar_ip(endereco_ip):
        print("IP inválido. Tente novamente.")
        endereco_ip = input("Digite o endereço IP: ")

    mascara_inicial = int(input("Digite a máscara de rede inicial (CIDR): "))
    mascara_final = int(input("Digite a máscara de rede final (CIDR): "))

    resultados = []

    for cidr in range(mascara_inicial, mascara_final + 1):
        mascara_bin = mascara_para_binario(cidr)
        mascara_pontuada = binario_para_decimal_pontuado(mascara_bin)
        mascara_inteiro = binario_para_inteiro(mascara_bin)

        ip_inteiro = ip_para_inteiro(endereco_ip)

        # Cálculo do endereço de rede
        endereco_rede = ip_inteiro // (2 ** (32 - cidr)) * (2 ** (32 - cidr))

        # Cálculo do endereço de broadcast
        endereco_broadcast = endereco_rede + (2 ** (32 - cidr)) - 1

        # Primeiro e último IP válidos
        primeiro_ip = endereco_rede + 1
        ultimo_ip = endereco_broadcast - 1

        # Conversão para strings com pontos
        endereco_rede_str = inteiro_para_ip(endereco_rede)
        endereco_broadcast_str = inteiro_para_ip(endereco_broadcast)
        primeiro_ip_str = inteiro_para_ip(primeiro_ip)
        ultimo_ip_str = inteiro_para_ip(ultimo_ip)

        hosts_validos = calcular_hosts(cidr)

        print(f"\nCIDR /{cidr}")
        print(f"Máscara: {mascara_pontuada}")
        print(f"Endereço de Rede: {endereco_rede_str}")
        print(f"Endereço de Broadcast: {endereco_broadcast_str}")
        print(f"Primeiro IP válido: {primeiro_ip_str}")
        print(f"Último IP válido: {ultimo_ip_str}")
        print(f"Hosts válidos: {hosts_validos}")

        resultados.append({
            "CIDR": f"/{cidr}",
            "Mascara_decimal": mascara_pontuada,
            "Mascara_binaria": mascara_bin,
            "Hosts_validos": hosts_validos,
            "Endereco_rede": endereco_rede_str,
            "Endereco_broadcast": endereco_broadcast_str,
            "Primeiro_ip_valido": primeiro_ip_str,
            "Ultimo_ip_valido": ultimo_ip_str
        })

    # Salva os resultados em um arquivo JSON
    with open("resultado_subredes.json", "w") as arquivo_json:
        json.dump(resultados, arquivo_json, indent=4)

    print("\nResultados salvos no arquivo 'resultado_subredes.json'.")

# Executa o programa
if __name__ == "__main__":
    calculadora_sub_rede()
