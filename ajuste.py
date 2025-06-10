import csv

with open('contacts.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    # Pula o cabeçalho
    next(csv_reader)
    
    # Percorre cada linha e tenta acessar o segundo caractere da coluna 30
    for row in csv_reader:
        if len(row) > 30 and len(row[30]) > 1:  # Verifica se o índice 30 existe e se a string tem mais de 1 caractere
            print(row[30][1])
