import csv

# Funções auxiliares

def extrair_numeros(contato):
    """
    Remove todos os caracteres que não são números.
    """
    return ''.join([char for char in contato if char.isdigit()])

def classificar_por_tamanho(contatos):
    """
    Classifica os números de telefone por comprimento e retorna listas apropriadas.
    """
    list_8, list_9, list_10, list_11, outros = [], [], [], [], []

    for contato in contatos:
        tamanho = len(contato)
        if tamanho == 8:
            list_8.append(contato)
        elif tamanho == 9:
            list_9.append(contato)
        elif tamanho == 10:
            list_10.append(contato)
        elif tamanho == 11:
            list_11.append(contato)
        else:
            outros.append(contato)

    return list_8, list_9, list_10, list_11, outros

def processar_outros(outros):
    """
    Processa números com mais de 11 dígitos e os classifica de acordo com prefixos conhecidos.
    """
    list_8, list_9, list_11 = [], [], []

    for contato in outros:
        if len(contato) > 11:
            if contato.startswith("84"):
                list_11.append(contato[:11])
            elif contato.startswith("9"):
                list_9.append(contato[:9])
            else:
                list_8.append(contato[:8])

    return list_8, list_9, list_11

def formatar_contatos(list_8, list_9, list_10, list_11):
    """
    Adiciona os prefixos apropriados para cada lista de números de telefone.
    """
    contatos_2 = []

    # Formatando números de 8 dígitos
    contatos_2 += [f'55849{num}' for num in list_8]
    
    # Formatando números de 9 dígitos
    contatos_2 += [f'5584{num}' for num in list_9]

    # Formatando números de 10 dígitos (ignora o primeiro dígito)
    contatos_2 += [f'55849{num[1:]}' for num in list_10]

    # Formatando números de 11 dígitos
    contatos_2 += [f'55{num}' for num in list_11]

    return contatos_2

# Código principal

contatos_iniciais = []

with open('contacts.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)  # Ignora a primeira linha (cabeçalho)

    # Coleta os números de telefone da coluna 30 (índice 29)
    contatos_iniciais = [extrair_numeros(row[30]) for row in csv_reader]

# Classificação dos números de telefone por tamanho
list_8, list_9, list_10, list_11, outros = classificar_por_tamanho(contatos_iniciais)

# Processamento de números fora dos padrões e redistribuição
outros_8, outros_9, outros_11 = processar_outros(outros)

# Adiciona os números redistribuídos às suas listas apropriadas
list_8 += outros_8
list_9 += outros_9
list_11 += outros_11

# Formatação final dos contatos
contatos_formatados = formatar_contatos(list_8, list_9, list_10, list_11)

# Imprimindo os contatos formatados para verificar
for contato in contatos_formatados:
    print(contato)
