from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

# Configurar o Selenium com Chrome headless
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Definir o driver global
driver = None

def iniciar_sessao_chatgpt():
    global driver
    if driver is None:
        driver = webdriver.Chrome(options=options)
        driver.get("https://chat.openai.com/")
        time.sleep(5)  # Esperar a página carregar

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")

    if driver is None:
        iniciar_sessao_chatgpt()

    # Enviar mensagem para o ChatGPT
    chat_input = driver.find_element(By.TAG_NAME, "textarea")
    chat_input.send_keys(user_message)
    chat_input.send_keys(Keys.RETURN)
    time.sleep(5)

    # Capturar resposta do ChatGPT
    messages = driver.find_elements(By.CLASS_NAME, "message")
    resposta = messages[-1].text if messages else "Erro ao obter resposta."

    return jsonify({"response": resposta})

if __name__ == "__main__":
    iniciar_sessao_chatgpt()
    app.run(host="0.0.0.0", port=5000)
