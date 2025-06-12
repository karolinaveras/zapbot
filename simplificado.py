import PySimpleGUI as sg
import csv
import time
from datetime import datetime
import pyautogui
import pyperclip
import re
import os

pyautogui.PAUSE = 1.5
pyautogui.FAILSAFE = True

class WhatsAppBot:
    def __init__(self, config):
        self.config = config
        self.contatos = self._processar_csv()
        
    def _processar_csv(self):
        """Carrega e processa os contatos do arquivo CSV com mensagens personalizadas"""
        contatos = []
        blacklist = {5584999949535, 5584999449835}
        
        with open(self.config['arquivo_csv'], newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Processa todos os campos de telefone encontrados
                for campo in ['Phone 1 - Value', 'Phone 2 - Value', 'Telefone', 'Celular']:
                    if campo in row and row[campo].strip():
                        num_limpo = self._limpar_numero(row[campo])
                        if num_limpo:
                            num_formatado = self._formatar_numero(num_limpo)
                            if num_formatado and int(num_formatado) not in blacklist:
                                # Adiciona mensagem personalizada se existir no CSV
                                mensagem = row.get('Mensagem', self.config.get('texto', ''))
                                contatos.append({
                                    'numero': num_formatado,
                                    'nome': row.get('Nome', ''),
                                    'mensagem': mensagem
                                })
                                break  # Usa o primeiro número válido encontrado
        
        return contatos
    
    def _limpar_numero(self, numero):
        """Remove caracteres não numéricos e valida formato"""
        if not numero:
            return None
            
        num_limpo = ''.join(c for c in numero if c.isdigit())
        
        # Validação básica de número brasileiro
        if len(num_limpo) < 8:  # Muito curto para ser válido
            return None
            
        return num_limpo
    
    def _formatar_numero(self, numero):
        """Formata o número para padrão internacional"""
        # Remove zeros e nones iniciais
        numero = numero.lstrip('0')
        
        # Se já começar com 55 (código do Brasil), assume que está completo
        if numero.startswith('55'):
            return numero if len(numero) >= 12 else None
            
        # Adiciona código do país e DDD padrão se necessário
        if len(numero) == 8:  # Número local
            return f'55849{numero}'
        elif len(numero) == 9:  # Celular sem DDD
            return f'5584{numero}'
        elif len(numero) == 10:  # Fixo com DDD
            return f'55{numero[1:]}'  # Remove o 0 inicial
        elif len(numero) == 11:  # Celular com DDD
            return f'55{numero}'
        else:
            return None
    
    def enviar_mensagens(self, window):
        """Executa o envio das mensagens com atualização de progresso"""
        total_envios = 0
        cont_erro = []
        total_contatos = len(self.contatos)
        
        for i, contato in enumerate(self.contatos):
            # Atualiza interface
            if window:
                window['-PROGRESS-'].update_bar(i + 1, total_contatos)
                window.refresh()
            
            resultado = self._enviar_para_contato(contato)
            
            if resultado['sucesso']:
                total_envios += 1
            else:
                cont_erro.append(contato['numero'])
                print(f"Erro no contato {contato['nome'] or contato['numero']}: {resultado['erro']}")
            
            time.sleep(self.config['intervalo_envio'])
        
        self._gerar_relatorio(total_envios, cont_erro)
        return total_envios, cont_erro
    
    def _enviar_para_contato(self, contato):
        """Tenta enviar mensagem para um contato específico"""
        resultado = {'sucesso': False, 'erro': None}
        link = f"https://api.whatsapp.com/send?phone={contato['numero']}"
        
        try:
            # Navega até o WhatsApp Web
            pyautogui.hotkey('ctrl', 'l')
            pyperclip.copy(link)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            time.sleep(5)
            
            # Verifica se o número é válido
            if self._verificar_erro():
                resultado['erro'] = "Número inválido ou não existe no WhatsApp"
                return resultado
            
            # Envia a mensagem
            pyautogui.click(self.config['coordenadas']['chat'])
            time.sleep(1)
            
            if contato['mensagem']:
                mensagem = self._personalizar_mensagem(contato['mensagem'], contato)
                pyperclip.copy(mensagem)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                time.sleep(2)
            
            # Envia mídia se configurado
            if self.config['enviar_midia']:
                if not self._enviar_midia():
                    resultado['erro'] = "Falha ao enviar mídia"
                    return resultado
            
            resultado['sucesso'] = True
            print(f"Mensagem enviada para {contato['nome'] or contato['numero']}")
            
        except Exception as e:
            resultado['erro'] = str(e)
        
        return resultado
    
    def _personalizar_mensagem(self, mensagem, contato):
        """Substitui placeholders na mensagem"""
        return mensagem.replace('{nome}', contato.get('nome', '')) \
                      .replace('{numero}', contato['numero'])
    
    def _verificar_erro(self):
        """Verifica se apareceu mensagem de erro"""
        try:
            # Tenta várias imagens de erro possíveis
            for img in ['erro.png', 'erro2.png', 'invalido.png']:
                if pyautogui.locateOnScreen(img, confidence=0.8) is not None:
                    return True
            return False
        except:
            return False
    
    def _enviar_midia(self):
        """Envia anexos conforme configurado"""
        try:
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
            return True
        except:
            return False
    
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
        
        # Cria pasta de relatórios se não existir
        os.makedirs('relatorios', exist_ok=True)
        nome_arquivo = f"relatorios/relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(nome_arquivo, 'a', encoding='utf-8') as f:
            f.write(relatorio)
        
        print(relatorio)
        return nome_arquivo

def criar_interface():
    """Cria e retorna a janela principal da interface gráfica"""
    sg.theme('DarkTeal9')
    
    layout = [
        [sg.Text('Arquivo CSV:'), sg.Input(key='-CSV-'), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
        [sg.Text('Mensagem padrão:')],
        [sg.Multiline(size=(50, 5), key='-TEXTO-', tooltip='Será usada se não houver mensagem no CSV')],
        [sg.Checkbox('Enviar mídia', key='-MIDIA-')],
        [sg.Text('Intervalo (segundos):'), sg.Input('5', size=(5,1), key='-INTERVALO-')],
        [sg.ProgressBar(max_value=100, orientation='h', size=(50, 20), key='-PROGRESS-')],
        [sg.Button('Iniciar', size=(10,1)), sg.Button('Sair', size=(10,1))],
        [sg.Output(size=(60, 10), key='-OUTPUT-')]
    ]
    
    return sg.Window('WhatsApp Bot - Envio Automático', layout, finalize=True)

def main():
    window = criar_interface()
    
    while True:
        event, values = window.read()
        
        if event in (sg.WINDOW_CLOSED, 'Sair'):
            break
            
        if event == 'Iniciar':
            if not values['-CSV-']:
                sg.popup_error('Selecione um arquivo CSV!')
                continue
                
            config = {
                'arquivo_csv': values['-CSV-'],
                'texto': values['-TEXTO-'],
                'enviar_midia': values['-MIDIA-'],
                'intervalo_envio': float(values['-INTERVALO-']),
                'coordenadas': {
                    'chat': (681, 354),
                    'clip': (485, 693),
                    'midia': (485, 637),
                    'area_trabalho': (86, 107),
                    'pasta': (237, 160)
                }
            }
            
            print("\n=== INICIANDO ENVIO ===")
            try:
                bot = WhatsAppBot(config)
                print(f"Total de contatos carregados: {len(bot.contatos)}")
                
                # Mostra pré-visualização do primeiro contato
                if bot.contatos:
                    primeiro = bot.contatos[0]
                    preview = f"\nPré-visualização do primeiro envio:\n"
                    preview += f"Número: {primeiro['numero']}\n"
                    preview += f"Nome: {primeiro.get('nome', 'Não informado')}\n"
                    preview += f"Mensagem: {primeiro['mensagem'][:50]}..." if primeiro['mensagem'] else "Sem mensagem"
                    print(preview)
                
                sg.popup_auto_close('Preparando... Posicione a janela do WhatsApp Web e aguarde', auto_close_duration=5)
                time.sleep(5)
                
                # Executa envios
                sucessos, erros = bot.enviar_mensagens(window)
                
                # Mostra resumo
                resumo = f"\n=== RESUMO ===\n"
                resumo += f"Total: {len(bot.contatos)}\n"
                resumo += f"Sucessos: {sucessos}\n"
                resumo += f"Erros: {len(erros)}\n"
                if erros:
                    resumo += f"\nNúmeros com erro:\n" + "\n".join(erros[:5])  # Mostra até 5 erros
                    if len(erros) > 5:
                        resumo += f"\n... e mais {len(erros)-5} números"
                print(resumo)
                
                sg.popup('Envio concluído!', f"Sucessos: {sucessos}\nErros: {len(erros)}")
                
            except Exception as e:
                print(f"Erro: {str(e)}")
                sg.popup_error(f'Ocorreu um erro:\n{str(e)}')

    window.close()

if __name__ == '__main__':
    main()
    