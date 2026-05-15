from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Cromi está despierta y activa."

def run():
    # Aquí es donde va el puerto, pero dentro de su función para que no se dispare solo
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # Esto crea un "hilo" secundario para que la web y el bot funcionen a la vez sin chocarse
    t = Thread(target=run)
    t.start()
