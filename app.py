
import os
from flask import Flask, render_template_string, request
import google.generativeai as genai

app = Flask(__name__)

# CONFIGURAÇÃO SEGURA: Ele vai ler a chave que vamos colocar no Render
api_key_env = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key_env)
model = genai.GenerativeModel('gemini-1.5-flash')

html_code = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BESTTEC SYSTEM - AI</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #0f172a; margin: 0; display: flex; align-items: center; justify-content: center; height: 100vh; }
        .chat-container { width: 95%; max-width: 450px; height: 85vh; background: #1e293b; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow: hidden; display: flex; flex-direction: column; border: 1px solid #334155; }
        .chat-header { background: #3b82f6; color: white; padding: 20px; text-align: center; font-weight: bold; font-size: 1.2rem; }
        #chat-window { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
        .input-area { display: flex; padding: 15px; background: #0f172a; border-top: 1px solid #334155; }
        input { flex: 1; padding: 12px; border: 1px solid #334155; background: #1e293b; color: white; border-radius: 25px 0 0 25px; outline: none; padding-left: 20px; }
        button { padding: 12px 25px; background-color: #3b82f6; color: white; border: none; border-radius: 0 25px 25px 0; cursor: pointer; font-weight: bold; }
        .msg { padding: 12px 16px; border-radius: 18px; max-width: 80%; font-size: 0.95rem; line-height: 1.5; color: white; }
        .user-msg { background-color: #3b82f6; align-self: flex-end; }
        .bot-msg { background-color: #334155; align-self: flex-start; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">BESTTEC SYSTEM</div>
        <div id="chat-window">
            <div class="msg bot-msg">Olá! <b>BESTTEC SYSTEM</b> configurada com sucesso. Como posso te ajudar?</div>
        </div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Digite sua mensagem...">
            <button onclick="sendMessage()">Enviar</button>
        </div>
    </div>
    <script>
        const chatWindow = document.getElementById('chat-window');
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;
            chatWindow.innerHTML += `<div class="msg user-msg">${message}</div>`;
            input.value = '';
            chatWindow.scrollTop = chatWindow.scrollHeight;
            try {
                const response = await fetch(`/chat?msg=${encodeURIComponent(message)}`);
                const data = await response.text();
                chatWindow.innerHTML += `<div class="msg bot-msg">${data}</div>`;
            } catch (err) {
                chatWindow.innerHTML += `<div class="msg bot-msg">Erro ao conectar com a IA. Verifique a chave no Render.</div>`;
            }
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
        document.getElementById('user-input').addEventListener('keypress', (e) => { if(e.key === 'Enter') sendMessage(); });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_code)

@app.route('/chat')
def chat():
    user_message = request.args.get('msg')
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"Erro na IA: {str(e)}"
