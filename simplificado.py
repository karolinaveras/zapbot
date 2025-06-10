import csv
import time
from datetime import datetime
import pyautogui
import pyperclip

pyautogui.PAUSE = 1.5  # Adiciona pequena pausa entre ações
pyautogui.FAILSAFE = True  # Permite abortar movendo mouse para canto

class WhatsAppBot:
    def __init__(self, config):
        self.config = config
        self.contatos = self._processar_csv()
        
    def _processar_csv(self):
        """Carrega e processa os contatos do arquivo CSV"""
        contatos_brutos = []
        blacklist = {5584999949535, 5584999449835}
        
        with open(self.config['arquivo_csv'], newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Processa ambos os campos de telefone
                for campo in ['Phone 1 - Value', 'Phone 2 - Value']:
                    if campo in row:
                        contatos_brutos.append(row[campo])
        
        # Processamento e formatação dos números
        contatos_formatados = set()
        for num in contatos_brutos:
            num_limpo = self._limpar_numero(num)
            if num_limpo:
                num_formatado = self._formatar_numero(num_limpo)
                if num_formatado and int(num_formatado) not in blacklist:
                    contatos_formatados.add(num_formatado)
        
        return list(contatos_formatados)
    
    def _limpar_numero(self, numero):
        """Remove caracteres não numéricos"""
        return ''.join(c for c in numero if c.isdigit())
    
    def _formatar_numero(self, numero):
        """Formata o número conforme padrões brasileiros"""
        tamanho = len(numero)
        
        if tamanho == 8:  # Número local (8 dígitos)
            return f'55849{numero}'
        elif tamanho == 9:  # Celular (9 dígitos)
            return f'5584{numero}'
        elif tamanho == 10:  # Fixo com DDD (10 dígitos)
            return f'55849{numero[1:]}'  # Remove o 0 inicial
        elif tamanho == 11:  # Celular com DDD (11 dígitos)
            return f'55{numero}'
        elif tamanho > 11:  # Números longos (trunca)
            if numero.startswith('84'):
                return f'55849{numero[2:11]}'
            elif numero.startswith('9'):
                return f'5584{numero[1:10]}'
            else:
                return f'55849{numero[:8]}'
        return None
    
    def enviar_mensagens(self):
        """Executa o envio das mensagens"""
        total_envios = 0
        cont_erro = []
        
        for numero in self.contatos:
            if self._enviar_para_numero(numero):
                total_envios += 1
            else:
                cont_erro.append(numero)
            
            time.sleep(self.config['intervalo_envio'])
        
        self._gerar_relatorio(total_envios, cont_erro)
    
    def _enviar_para_numero(self, numero):
        """Tenta enviar mensagem para um número específico"""
        link = f"https://api.whatsapp.com/send?phone={numero}"
        
        # Navega até o WhatsApp Web
        pyautogui.hotkey('ctrl', 'l')
        pyperclip.copy(link)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(5)
        
        # Verifica se o número é válido
        if self._verificar_erro():
            print(f"Erro no número: {numero}")
            return False
        
        # Envia a mensagem
        pyautogui.click(self.config['coordenadas']['chat'])
        time.sleep(1)
        
        if self.config['texto']:
            pyperclip.copy(self.config['texto'])
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            time.sleep(2)
        
        # Envia mídia se configurado
        if self.config['enviar_midia']:
            self._enviar_midia()
        
        return True
    
    def _verificar_erro(self):
        """Verifica se apareceu mensagem de erro"""
        try:
            return pyautogui.locateOnScreen('erro.png') is not None
        except:
            return False
    
    def _enviar_midia(self):
        """Envia anexos conforme configurado"""
        pyautogui.click(self.config['coordenadas']['clip'])
        time.sleep(1)
        pyautogui.click(self.config['coordenadas']['midia'])
        time.sleep(2)
        pyautogui.click(self.config['coordenadas']['area_trabalho'])
        time.sleep(1)
        pyautogui.doubleClick(self.config['coordenadas']['pasta'])
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('enter')
        time.sleep(9)
        pyautogui.press('enter')
    
    def _gerar_relatorio(self, total_envios, cont_erro):
        """Gera relatório final"""
        relatorio = f"""
        {datetime.now().strftime('%d/%m/%Y %H:%M')}
        Arquivo CSV: {self.config['arquivo_csv']}
        Total de contatos: {len(self.contatos)}
        Envios realizados: {total_envios}
        Erros: {len(cont_erro)}
        Números com erro: {cont_erro if cont_erro else 'Nenhum'}
        """
        
        with open('relatorio.txt', 'a') as f:
            f.write(relatorio)
        
        print(relatorio)

# Configuração do bot
config = {
    'arquivo_csv': 'contatos.csv',
    'texto': 'Olá, esta é uma mensagem automática!',
    'enviar_midia': False,
    'intervalo_envio': 5,
    'coordenadas': {
        'chat': (681, 354),
        'clip': (485, 693),
        'midia': (485, 637),
        'area_trabalho': (86, 107),
        'pasta': (237, 160)
    }
}

# Execução
if __name__ == '__main__':
    print("Iniciando bot em 5 segundos...")
    time.sleep(5)
    bot = WhatsAppBot(config)
    bot.enviar_mensagens()