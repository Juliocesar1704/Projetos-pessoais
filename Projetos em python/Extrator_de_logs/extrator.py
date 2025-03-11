import csv  # Importa o módulo para manipulação de arquivos CSV
import tkinter as tk  # Importa o módulo tkinter para criar interfaces gráficas
from tkinter import filedialog  # Importa o submódulo filedialog para abrir a janela de seleção de arquivos
import re  # Importa o módulo de expressões regulares para buscar padrões no log
import json  # Importa o módulo JSON para exportar dados no formato JSON
import pandas as pd  # Importa o pandas para trabalhar com dados e exportar para Excel
import os  # Importa o módulo os para manipular caminhos de arquivos

# Função para selecionar o arquivo de log
def selecionar_arquivo():
    """
    Abre uma janela de seleção de arquivo para o usuário escolher um arquivo de log.
    Se o usuário não selecionar um arquivo, o programa será encerrado.
    """
    root = tk.Tk()  # Cria a janela principal do Tkinter
    root.withdraw()  # Esconde a janela principal, pois não é necessária para a interface gráfica
    # Abre a janela de seleção de arquivo, filtrando para mostrar apenas arquivos .txt
    arquivo_selecionado = filedialog.askopenfilename(title="Selecione um arquivo de log", filetypes=[("Arquivos de Texto", "*.txt")])
    # Se o usuário cancelar a seleção de arquivo, encerra o programa
    if not arquivo_selecionado:
        print("Nenhum arquivo selecionado. Encerrando o programa.")
        exit()  # Encerra o programa
    return arquivo_selecionado  # Retorna o caminho do arquivo selecionado

# Função para ler o arquivo de log e extrair os dados
def ler_arquivo_log(nome_arquivo):
    """
    Lê o arquivo de log e processa cada linha, extraindo os dados de interesse.
    """
    dados_extraidos = []  # Lista para armazenar os dados extraídos de cada linha do arquivo
    with open(nome_arquivo, "r") as arquivo:  # Abre o arquivo de log em modo leitura
        for linha in arquivo:  # Itera por cada linha do arquivo
            dados_linha = parse_log_line(linha)  # Chama a função para processar a linha
            if dados_linha:  # Se a linha foi processada corretamente (não retornou None)
                dados_extraidos.append(dados_linha)  # Adiciona os dados extraídos à lista
    return dados_extraidos  # Retorna a lista de dados extraídos

# Função para analisar e extrair os dados de uma linha de log
def parse_log_line(linha):
    """
    Analisa uma linha de log e extrai informações como IP, data, método HTTP, código, etc.
    Utiliza expressões regulares para identificar e capturar os campos.
    """
    # Expressão regular para capturar os dados típicos de um log de servidor (Apache/Nginx)
    regex = r'(?P<ip>\d+\.\d+\.\d+\.\d+)'  # Captura o endereço IP (exemplo: 192.168.1.1)
    regex += r' \- \- \[(?P<data_hora>[^\]]+)\]'  # Captura a data e hora da requisição (exemplo: 12/Apr/2025:10:15:30)
    regex += r' "(?P<metodo>\w+) (?P<request>.*?) HTTP/\d\.\d"'  # Captura o método HTTP e o caminho solicitado
    regex += r' (?P<codigo>\d{3})'  # Captura o código de status HTTP (exemplo: 200, 404)
    regex += r' (?P<bytes>\d+)'  # Captura o número de bytes da resposta (exemplo: 1024)
    regex += r' "(?P<referrer>.*?)"'  # Captura o referenciador (referer) da requisição
    regex += r' "(?P<user_agent>.*?)"'  # Captura o User-Agent (informações sobre o navegador ou bot)

    match = re.match(regex, linha)  # Aplica a expressão regular na linha do log
    if match:  # Se houver correspondência, retorna os dados extraídos como um dicionário
        return match.groupdict()  # Retorna um dicionário com os dados extraídos
    return None  # Se não houver correspondência, retorna None, ignorando a linha

# Função para agrupar os dados conforme os campos desejados
def agrupar_dados(dados, campos_para_agrupamento):
    """
    Agrupa os dados conforme os campos selecionados pelo usuário.
    """
    dados_agrupados = {}  # Dicionário para armazenar as chaves de agrupamento e suas respectivas contagens

    for linha in dados:  # Itera sobre todos os dados extraídos
        # Cria uma chave de agrupamento que será uma tupla com os valores dos campos selecionados
        chave_agrupamento = tuple(linha[campo] for campo in campos_para_agrupamento)
        
        if chave_agrupamento not in dados_agrupados:  # Se a chave ainda não existir, inicializa com 0
            dados_agrupados[chave_agrupamento] = 0
        dados_agrupados[chave_agrupamento] += 1  # Incrementa a contagem para a chave de agrupamento

    return dados_agrupados  # Retorna o dicionário com os dados agrupados e suas contagens

# Função para exportar os dados agrupados para um arquivo CSV
def exportar_para_csv(dados_agrupados, campos, nome_arquivo_saida):
    """
    Exporta os dados agrupados para um arquivo CSV.
    """
    dados_ordenados = sorted(dados_agrupados.items(), key=lambda x: x[1], reverse=True)  # Ordena os dados pela contagem
    with open(nome_arquivo_saida, 'w', newline='') as csvfile:  # Abre o arquivo CSV para escrita
        writer = csv.writer(csvfile)  # Cria um objeto escritor para o CSV
        writer.writerow(['Quantidade de requests'] + campos)  # Escreve o cabeçalho com a quantidade de requests e os campos selecionados
        # Escreve os dados agrupados no arquivo CSV
        for chave, contagem in dados_ordenados:
            writer.writerow([contagem] + list(chave))  # Escreve a contagem seguida pelos valores dos campos
    print(f"Dados exportados para {nome_arquivo_saida}")

# Função para exportar os dados agrupados para um arquivo JSON
def exportar_para_json(dados_agrupados, nome_arquivo_saida):
    """
    Exporta os dados agrupados para um arquivo JSON.
    """
    # Convertendo as tuplas de chaves para listas
    dados_agrupados_convertidos = {str(chave): valor for chave, valor in dados_agrupados.items()}

    # Agora podemos salvar o dicionário convertido como JSON
    with open(nome_arquivo_saida, 'w') as jsonfile:  # Abre o arquivo JSON para escrita
        json.dump(dados_agrupados_convertidos, jsonfile, indent=4)  # Salva os dados como JSON no arquivo
    print(f"Dados exportados para {nome_arquivo_saida}")

# Função para exportar os dados agrupados para um arquivo Excel usando Pandas
def exportar_para_excel(dados_agrupados, campos, nome_arquivo_saida):
    """
    Exporta os dados agrupados para um arquivo Excel usando pandas.
    """
    # Converte os dados agrupados para um formato adequado para o pandas DataFrame
    dados_agrupados_lista = [
        [contagem] + list(chave) for chave, contagem in dados_agrupados.items()
    ]
    
    # Cria um DataFrame com pandas
    df = pd.DataFrame(dados_agrupados_lista, columns=['Quantidade de requests'] + campos)
    
    # Salva o DataFrame em um arquivo Excel
    df.to_excel(nome_arquivo_saida, index=False)  # index=False para não incluir o índice como coluna
    print(f"Dados exportados para {nome_arquivo_saida}")

# Função para pedir ao usuário os campos a serem extraídos
def solicitar_campos_agrupamento():
    """
    Solicita ao usuário os campos para agrupamento (exemplo: 'ip', 'codigo').
    """
    # Campos disponíveis para agrupamento (são os campos que podem ser escolhidos pelo usuário)
    campos_disponiveis  = [ 'ip' , 'data_hora' , 'metodo' , 'request' , 'codigo' , 'bytes' , 'referrer' , 'user_agent' ]
    
    # Exibe os campos disponíveis para o usuário escolher
    print ( "="  *  75 )   # Exibe uma linha
    print ( "Arquivo de log carregado com sucesso!" . center ( 72 ), ' \n ' ) # Exibe uma mensagem de sucesso
    print ( "Campos disponíveis" . center ( 72 ), ' \n ' ) # Exibe uma mensagem baixar os campos disponíveis
    print ( " | " . join ( campos_disponiveis ))   # Exibe os campos possíveis
    print ( "="  *  75 ) # Exibe uma linha de separação
    
    campos_selecionados = input("Digite os campos desejados para agrupamento separados por vírgula: ").split(',')
    campos_selecionados = [campo.strip() for campo in campos_selecionados]  # Remove espaços extras
    # Verifica se todos os campos informados são válidos
    campos_invalidos = [campo for campo in campos_selecionados if campo not in campos_disponiveis]
    
    if campos_invalidos:
        print(f"Campos inválidos: {', '.join(campos_invalidos)}. Por favor, tente novamente.")
        return solicitar_campos_agrupamento()  # Chama novamente caso campos inválidos sejam fornecidos
    
    return campos_selecionados  # Retorna a lista de campos selecionados pelo usuário

# Função para solicitar o formato de exportação
def solicitar_formato_exportacao():
    """
    Solicita ao usuário o formato para exportação dos dados (CSV, JSON ou Excel).
    """
    formatos_disponiveis = ['csv', 'json', 'excel']  # Formatos disponíveis
    print("Formatos de exportação disponíveis: CSV, JSON, Excel")
    formato_selecionado = input("Escolha o formato desejado (csv, json, excel): ").lower()
    
    if formato_selecionado not in formatos_disponiveis:
        print("Formato inválido. Por favor, tente novamente.")
        return solicitar_formato_exportacao()  # Chama novamente caso o formato seja inválido
    
    return formato_selecionado  # Retorna o formato escolhido

# Função principal do programa
def main():
    """
    Função principal que orquestra todo o fluxo: seleção de arquivo, processamento de dados,
    agrupamento e exportação para CSV, JSON ou Excel.
    """
    nome_arquivo = selecionar_arquivo()  # Chama a função para selecionar o arquivo de log
    dados = ler_arquivo_log(nome_arquivo)  # Lê e processa os dados do log

    # Solicita ao usuário os campos para agrupamento
    campos_agrupamento = solicitar_campos_agrupamento()  # Agora o usuário escolhe os campos para agrupamento
    
    dados_agrupados = agrupar_dados(dados, campos_agrupamento)  # Agrupa os dados conforme os campos selecionados

    # Solicita o formato de exportação
    formato_exportacao = solicitar_formato_exportacao()

    # Exporta os dados agrupados no formato escolhido
    if formato_exportacao == 'csv':
        exportar_para_csv(dados_agrupados, campos_agrupamento, "analise_log.csv")
    elif formato_exportacao == 'json':
        exportar_para_json(dados_agrupados, "analise_log.json")
    elif formato_exportacao == 'excel':
        exportar_para_excel(dados_agrupados, campos_agrupamento, "analise_log.xlsx")

if __name__ == "__main__":
    main()  # Chama a função principal
