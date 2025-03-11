import csv
import tkinter as tk
from tkinter import filedialog
import re

# Função para selecionar o arquivo de log
def selecionar_arquivo():
    """
    Abre uma janela de seleção de arquivo para o usuário escolher um arquivo de log.
    Se o usuário não selecionar um arquivo, o programa será encerrado.
    """
    # Cria a janela principal do Tkinter, mas a esconde para não exibir uma janela desnecessária
    root = tk.Tk()
    root.withdraw()
    
    # Abre a janela de seleção de arquivo. O título é 'Selecione um arquivo de log' e o filtro de tipos é para arquivos .txt
    arquivo_selecionado = filedialog.askopenfilename(title="Selecione um arquivo de log", filetypes=[("Arquivos de Texto", "*.txt")])
    
    # Se nenhum arquivo for selecionado (caso o usuário cancele), o programa será encerrado
    if not arquivo_selecionado:
        print("Nenhum arquivo selecionado. Encerrando o programa.")
        exit()
    
    return arquivo_selecionado  # Retorna o caminho do arquivo selecionado

# Função para ler o arquivo de log e extrair os dados
def ler_arquivo_log(nome_arquivo):
    """
    Lê o arquivo de log e processa cada linha, extraindo os dados de interesse.
    """
    dados_extraidos = []  # Lista que armazenará os dados extraídos de cada linha do arquivo

    # Abre o arquivo de log para leitura (modo 'r')
    with open(nome_arquivo, "r") as arquivo:
        for linha in arquivo:  # Itera por cada linha do arquivo de log
            # Tenta extrair os dados da linha usando a função parse_log_line
            dados_linha = parse_log_line(linha)
            if dados_linha:  # Se a linha foi corretamente processada, adiciona ao resultado
                dados_extraidos.append(dados_linha)

    return dados_extraidos  # Retorna a lista de dados extraídos de todas as linhas do arquivo

# Função para analisar e extrair os dados de uma linha de log
def parse_log_line(linha):
    """
    Analisa uma linha de log e extrai informações como IP, data, método HTTP, código, etc.
    Utiliza expressões regulares para identificar e capturar os campos.
    """
    # Expressão regular que captura os dados típicos de um log de servidor (formato Apache/Nginx)
    regex = r'(?P<ip>\d+\.\d+\.\d+\.\d+)'  # Captura o endereço IP (exemplo: 192.168.1.1)
    regex += r' \- \- \[(?P<data_hora>[^\]]+)\]'  # Captura a data e hora da requisição (exemplo: 12/Apr/2025:10:15:30)
    regex += r' "(?P<metodo>\w+) (?P<request>.*?) HTTP/\d\.\d"'  # Captura o método HTTP e o caminho solicitado (exemplo: "GET /index.html HTTP/1.1")
    regex += r' (?P<codigo>\d{3})'  # Captura o código de status HTTP (exemplo: 200, 404)
    regex += r' (?P<bytes>\d+)'  # Captura o número de bytes da resposta (exemplo: 1024)
    regex += r' "(?P<referrer>.*?)"'  # Captura o referenciador (referer) da requisição, que indica de onde veio a requisição
    regex += r' "(?P<user_agent>.*?)"'  # Captura o User-Agent (informações sobre o navegador ou bot que fez a requisição)

    # Aplica a expressão regular na linha do log para tentar extrair os dados
    match = re.match(regex, linha)
    
    # Se a linha corresponde ao padrão da expressão regular, retorna os dados extraídos como um dicionário
    if match:
        return match.groupdict()  # Retorna os dados como um dicionário (ex.: {'ip': '192.168.1.1', 'data_hora': '12/Apr/2025:10:15:30', ...})
    return None  # Se a linha não corresponder ao formato esperado, retorna None (ignorando essa linha)

# Função para agrupar os dados conforme os campos desejados
def agrupar_dados(dados, campos_para_agrupamento):
    """
    Agrupa os dados conforme os campos selecionados pelo usuário.
    """
    dados_agrupados = {}  # Dicionário que armazenará as chaves de agrupamento e suas respectivas contagens

    # Para cada linha de dados extraídos, cria uma chave para agrupamento com base nos campos escolhidos
    for linha in dados:
        # Cria uma chave de agrupamento, que é uma tupla com os valores dos campos selecionados
        chave_agrupamento = tuple(linha[campo] for campo in campos_para_agrupamento)
        
        # Se a chave ainda não existir no dicionário, inicializa com 0
        if chave_agrupamento not in dados_agrupados:
            dados_agrupados[chave_agrupamento] = 0
        
        # Incrementa a contagem para a chave de agrupamento
        dados_agrupados[chave_agrupamento] += 1

    return dados_agrupados  # Retorna o dicionário com os dados agrupados e as contagens

# Função para exportar os dados agrupados para um arquivo CSV
def exportar_para_csv(dados_agrupados, campos, nome_arquivo_saida):
    """
    Exporta os dados agrupados para um arquivo CSV.
    A primeira coluna será a contagem de requisições, e as outras colunas os campos de agrupamento.
    """
    # Ordena os dados agrupados pela quantidade de requisições (da maior para a menor)
    dados_ordenados = sorted(dados_agrupados.items(), key=lambda x: x[1], reverse=True)

    # Cria e abre o arquivo CSV para escrita
    with open(nome_arquivo_saida, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)  # Cria o objeto escritor de CSV
        # Escreve o cabeçalho com a quantidade de requests e os campos escolhidos
        writer.writerow(['Quantidade de requests'] + campos)
        
        # Escreve os dados agrupados no arquivo CSV
        for chave, contagem in dados_ordenados:
            # Para cada chave de agrupamento, escreve a contagem seguida pelos valores dos campos
            writer.writerow([contagem] + list(chave))

# Função principal do programa
def main():
    """
    Função principal que orquestra todo o fluxo: seleção de arquivo, processamento de dados,
    agrupamento e exportação para CSV.
    """
    # Abre a janela para o usuário selecionar o arquivo de log
    nome_arquivo = selecionar_arquivo()  # Chama a função para selecionar o arquivo de log
    dados_extraidos = ler_arquivo_log(nome_arquivo)  # Lê o arquivo e extrai os dados

    # Campos disponíveis para agrupamento (são os campos que podem ser escolhidos pelo usuário)
    campos_disponiveis = ['ip', 'data_hora', 'metodo', 'request', 'codigo', 'bytes', 'referrer', 'user_agent']
    
    # Exibe os campos disponíveis para o usuário escolher
    print("=" * 72)
    print("Campos disponíveis".center(72), '\n')
    print(" | ".join(campos_disponiveis))  # Exibe os campos possíveis
    print("=" * 72)
    
    # Solicita ao usuário os campos que deseja agrupar
    campos_selecionados = [campo.strip() for campo in input("Digite os campos desejados separados por vírgula: ").split(',')]

    # Valida se os campos selecionados são válidos
    campos_selecionados = [campo for campo in campos_selecionados if campo in campos_disponiveis]
    if not campos_selecionados:
        # Se nenhum campo válido for selecionado, encerra o programa
        print("Nenhum campo válido selecionado. Encerrando o programa.")
        exit()

    # Agrupa os dados de acordo com os campos escolhidos
    dados_agrupados = agrupar_dados(dados_extraidos, campos_selecionados)

    # Define o nome do arquivo de saída para o CSV
    nome_arquivo_saida = 'analise.csv'

    # Exporta os dados agrupados para o arquivo CSV
    exportar_para_csv(dados_agrupados, campos_selecionados, nome_arquivo_saida)
    print(f"Dados exportados para {nome_arquivo_saida}")  # Exibe uma mensagem indicando que os dados foram exportados com sucesso

# Inicia o programa
if __name__ == "__main__":
    main()  # Chama a função principal para iniciar a execução do programa
