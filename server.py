import time
from datetime import datetime
import pyautogui
import pyperclip
from LeituraCSV import CsvRead

# Configurações principais
RESOLUCAO_TELA = (1366, 768)  # Defina a resolução da tela
NOME_ARQUIVO_CSV = 'contatos.csv'  # Arquivo CSV contendo os números de telefone
TEXTO = ''  # Texto a ser enviado
ENVIAR_MIDIA = False  # Defina como True para enviar mídias

# Coordenadas específicas de elementos na tela
COORDENADAS_BARRA_LINK = (947, 52)
COORDENADAS_CHAT = (681, 354)
COORDENADAS_CLIP = (485, 693)
COORDENADAS_MIDIA = (485, 637)
COORDENADAS_AREA_TRABALHO = (86, 107)
COORDENADAS_PASTA = (237, 160)

# Definição da API de WhatsApp
API_WHATSAPP = 'https://api.whatsapp.com/send?phone='

# Leitura dos contatos no CSV
condominio = CsvRead(NOME_ARQUIVO_CSV)
contatos = condominio.contatos

# Funções auxiliares
def copiar_para_area_de_transferencia(conteudo):
    pyperclip.copy(conteudo)
    pyautogui.hotkey('ctrl', 'v')

def mover_e_clicar(coordenada, clicks=1, intervalo=0.1):
    pyautogui.moveTo(coordenada)
    pyautogui.click(clicks=clicks, interval=intervalo)

def enviar_mensagem_erro(x):
    print(f"\nO Número {x} não possui WhatsApp")

def verificar_erro(numero):
    for _ in range(5):  # Tentar encontrar a imagem do erro até 5 vezes
        loc = pyautogui.locateOnScreen('Outros/Erro.PNG')
        if loc:
            enviar_mensagem_erro(numero)
            return True
    return False

def enviar_mensagem(texto):
    copiar_para_area_de_transferencia(texto)
    pyautogui.press('enter')
    time.sleep(2)

def enviar_midias():
    mover_e_clicar(COORDENADAS_CLIP)
    time.sleep(1)
    mover_e_clicar(COORDENADAS_MIDIA)
    time.sleep(2)
    mover_e_clicar(COORDENADAS_AREA_TRABALHO)
    time.sleep(1)
    mover_e_clicar(COORDENADAS_PASTA, clicks=2)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('enter')
    time.sleep(9)
    pyautogui.press('enter')

def processar_contatos(contatos, enviar_midia, texto):
    total_envios = 0
    cont_erro = []

    for numero in contatos:
        link = f"{API_WHATSAPP}{numero}"
        mover_e_clicar(COORDENADAS_BARRA_LINK)
        copiar_para_area_de_transferencia(link)
        pyautogui.press('enter')
        time.sleep(5)

        mover_e_clicar(COORDENADAS_CHAT)
        time.sleep(5)

        if verificar_erro(numero):
            cont_erro.append(numero)
            continue

        if texto:
            enviar_mensagem(texto)

        if enviar_midia:
            enviar_midias()

        total_envios += 1
        print(f"\nÚltimo contato enviado: {numero}")

        # Voltar para a página anterior
        pyautogui.hotkey('alt', 'tab')
        time.sleep(5)

    return total_envios, cont_erro

def gerar_relatorio(total, cont_erro):
    date = datetime.now().strftime('%d/%m/%Y %H:%M')

    with open("Relatorio.txt", "a") as arquivo:
        arquivo.write("------------------------------------------\n")
        arquivo.write(f"Condominio: {NOME_ARQUIVO_CSV}\n")
        arquivo.write(f"Data: {date}\n")
        arquivo.write(f"Texto: {TEXTO}\n\n")
        arquivo.write(f"Total de contatos: {len(condominio.contatos_iniciais)}\n")
        arquivo.write(f"Contatos removidos: {len(condominio.contatos_iniciais) - len(condominio.contatos)}\n")
        arquivo.write(f"Total de envios: {total}\n")
        if cont_erro:
            arquivo.write(f"Total de Erros: {len(cont_erro)}\n")
            arquivo.write(f"Números que deram erro: {cont_erro}\n")

# Programa principal
time.sleep(10)  # Aguarda 10 segundos antes de iniciar

total_envios, cont_erro = processar_contatos(contatos, ENVIAR_MIDIA, TEXTO)

# Voltar para a página original
pyautogui.hotkey('alt', 'tab', presses=2)

# Gera o relatório final
gerar_relatorio(total_envios, cont_erro)

print("\n------------------------------------------")
print(f"Total de contatos: {len(condominio.contatos_iniciais)}")
print(f"Contatos removidos: {len(condominio.contatos_iniciais) - len(condominio.contatos)}")
print(f"Total de envios: {total_envios}")
if cont_erro:
    print(f"Total de Erros: {len(cont_erro)}")
    print("Números que deram erro: ", cont_erro)

