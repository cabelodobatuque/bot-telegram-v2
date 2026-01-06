import os
import json
import requests
from http.server import BaseHTTPRequestHandler

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN' )

def send_telegram_message(chat_id, text):
    if not TELEGRAM_TOKEN:
        print("ERRO: TELEGRAM_TOKEN não definido")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10 )
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar mensagem: {str(e)}")
        return False

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            
            if content_length == 0:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True}).encode())
                return
            
            body = self.rfile.read(content_length)
            update = json.loads(body)
            
            if 'message' not in update:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True}).encode())
                return
            
            message = update['message']
            chat_id = message['chat']['id']
            user_text = message.get('text', '').strip()
            
            if user_text == '/start':
                response_text = "🤖 Olá! Bem-vindo ao Bot de Vídeos Virais!\n\nEnvie /criarvideo para começar."
            elif user_text == '/criarvideo':
                response_text = "🎬 Recebi seu pedido!\n\nIniciando o processo de criação de vídeo...\n\nEm breve, mais funcionalidades estarão disponíveis!"
            elif user_text.startswith('/'):
                response_text = f"❓ Comando desconhecido: {user_text}\n\nTente /start ou /criarvideo"
            else:
                response_text = f"✅ Você disse: {user_text}"
            
            send_telegram_message(chat_id, response_text)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': True}).encode())
            
        except Exception as e:
            print(f"ERRO NO HANDLER: {str(e)}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode())
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok', 'message': 'Bot is running'}).encode())
    
    def log_message(self, format, *args):
        pass
