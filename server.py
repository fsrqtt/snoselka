from flask import Flask, request
from psychic_snoser import main  # твой основной функционал

app = Flask(__name__)

@app.route('/')
def index():
    return "Snoser is online!"

@app.route('/run', methods=['POST'])
def run():
    main()  # вызываем твой основной код
    return "Script executed."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
