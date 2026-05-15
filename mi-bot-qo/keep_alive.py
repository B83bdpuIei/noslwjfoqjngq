from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# Tiene que ser 0.0.0.0 para que Render lo detecte, no dejes que el host esté vacío.
    app.run(host='0.0.0.0', port=8080)
