# **🤖 WhatsApp Bot - Envio Automático de Mensagens**  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  
![PySimpleGUI](https://img.shields.io/badge/GUI-PySimpleGUI-green)  
![Selenium](https://img.shields.io/badge/Automation-PyAutoGUI-red)  

**Um bot em Python para envio automático de mensagens e arquivos via WhatsApp Web.**  

🔹 **Envie mensagens em massa** para uma lista de contatos  
🔹 **Suporte a anexos** (documentos, imagens, etc.)  
🔹 **Interface gráfica amigável** (GUI)  
🔹 **Relatórios detalhados** de envios  

---

## **📌 Pré-requisitos**  
- Python 3.8+  
- Bibliotecas:  
  ```bash
  pip install PySimpleGUI pyautogui pyperclip pandas
  ```
- WhatsApp Web aberto no navegador (Chrome/Firefox)  

---

## **🚀 Como Usar**  
1. **Preparar o arquivo CSV**  
   - Formato recomendado:  
     ```csv
     Nome,Telefone,Mensagem
     João Silva,5584999999999,Olá {nome}, esta é uma mensagem automática!
     Maria Souza,5584888888888,Oi Maria, tudo bem?
     ```
   - **Placeholders** disponíveis:  
     - `{nome}` → Substitui pelo nome do contato  
     - `{numero}` → Substitui pelo número de telefone  

2. **Executar o Bot**  
   ```bash
   python simplificado.py
   ```
   - Selecione o arquivo CSV  
   - Defina a mensagem padrão (caso não haja no CSV)  
   - Ajuste o intervalo entre envios (em segundos)  

3. **Posicione a janela do WhatsApp Web**  
   - O bot usará coordenadas pré-definidas (ajustáveis no código).  

---

## **⚙️ Funcionalidades**  
✅ **Envio personalizado** (mensagens únicas por contato)  
✅ **Suporte a mídia** (envie PDFs, imagens, etc.)  
✅ **Blacklist de números** (evite enviar para contatos indesejados)  
✅ **Geração de relatórios** (salvo em `relatorios/`)  
✅ **Interface intuitiva** com barra de progresso  

---

## **📂 Estrutura do Projeto**  
```
whatsapp-bot/  
├── simplificado.py      # Código principal  
├── contatos.csv        # Exemplo de lista de contatos  
├── relatorios/         # Pasta com logs de execução  
└── README.md           # Este arquivo  
```

---

## **⚠️ Limitações e Avisos**  
- **Não faça spam!** O WhatsApp pode **banir** seu número se enviar muitas mensagens em curto período.  
- Mantenha um **intervalo seguro** entre envios (5-10 segundos).  
- O bot depende de **coordenadas de tela** — pode precisar de ajustes para diferentes resoluções.  

---

## **💡 Contribuição**  
Contribuições são bem-vindas! Sinta-se à vontade para:  
- Reportar **bugs** (issues)  
- Sugerir **melhorias**  
- Enviar **pull requests**  

---

## **📜 Licença**  
[MIT](https://choosealicense.com/licenses/mit/) → Use livremente para fins pessoais ou comerciais.  

---

### **✨ Dúvidas?**  
Entre em contato: **vtechbra@gmail.com**  

---

### **🔗 Links Úteis**  
- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)  
- [PySimpleGUI Examples](https://pysimplegui.readthedocs.io/)  
