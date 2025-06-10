import csv

class CsvRead:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.contatos = []
        self.contatos_iniciais = []
        self.blacklist = [5584999949535, 5584999449835]  # Números que não devem ser incluídos
        self.num_validos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # Leitura e processamento inicial dos contatos
        self._ler_contatos()
        self._processar_contatos()

    def _ler_contatos(self):
        """
        Lê o arquivo CSV e armazena os números de telefone nas listas apropriadas.
        """
        contatos_i = []

        with open(self.nome_arquivo, newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            next(csv_reader)  # Pular o cabeçalho

            for row in csv_reader:
                contatos_i.append(row['Phone 1 - Value'])
                contatos_i.append(row['Phone 2 - Value'])

        self.contatos_iniciais = contatos_i

    def _processar_contatos(self):
        """
        Processa os números lidos, removendo caracteres inválidos, formatando-os e eliminando duplicatas.
        """
        contatos_limpados = []
        for contato in self.contatos_iniciais:
            contato_limpo = self._extrair_numeros(contato)
            if contato_limpo:
                contatos_limpados.append(contato_limpo)

        contatos_formatados = self._formatar_contatos(contatos_limpados)

        # Elimina duplicatas e números da blacklist
        self.contatos = self._remover_duplicados(contatos_formatados)

    def _extrair_numeros(self, contato):
        """
        Extrai apenas os números de um contato (removendo outros caracteres).
        """
        return ''.join([char for char in contato if char in self.num_validos])

    def _formatar_contatos(self, contatos):
        """
        Formata os números de telefone conforme seu tamanho e localiza-os na lista apropriada.
        """
        contatos_formatados = []

        for contato in contatos:
            tamanho = len(contato)
            if tamanho == 8:  # Número de 8 dígitos
                contatos_formatados.append(f'55849{contato}')
            elif tamanho == 9:  # Número de 9 dígitos
                contatos_formatados.append(f'5584{contato}')
            elif tamanho == 10:  # Número de 10 dígitos (fixo local)
                contatos_formatados.append(f'55849{contato[1:]}')  # Remove o 0 inicial
            elif tamanho == 11:  # Número completo de celular
                contatos_formatados.append(f'55{contato}')
            elif tamanho > 11:  # Para números maiores que 11, assume que está correto e apenas corta o excesso
                if contato.startswith('84'):
                    contatos_formatados.append(f'55849{contato[2:]}')
                elif contato.startswith('9'):
                    contatos_formatados.append(f'5584{contato[1:]}')
                else:
                    contatos_formatados.append(f'55849{contato[:8]}')

        return contatos_formatados

    def _remover_duplicados(self, contatos):
        """
        Remove números duplicados e números presentes na blacklist.
        """
        contatos_unicos = []
        for contato in contatos:
            if contato not in contatos_unicos and int(contato) not in self.blacklist:
                contatos_unicos.append(int(contato))
        return contatos_unicos

    def remover_duplicados(self, lista_principal, lista2):
        """
        Remove números duplicados comparando duas listas.
        """
        return [x for x in lista_principal if x not in lista2 and x not in self.blacklist]

    def remover_ate(self, ultimo_contato):
        """
        Remove os contatos até um contato específico e atualiza a lista de contatos.
        """
        gatilho = False
        contatos_filtrados = []

        for contato in self.contatos_iniciais:
            if gatilho:
                if contato not in contatos_filtrados and contato not in self.blacklist:
                    contatos_filtrados.append(contato)
            if contato == ultimo_contato:
                gatilho = True

        self.contatos = contatos_filtrados
