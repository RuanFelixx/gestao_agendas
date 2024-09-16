from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def inicial():
    return render_template('inicial.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nome_da_atividade = request.form['nome_da_atividade']
        return render_template('form.html', nome_da_atividade=nome_da_atividade)
    return render_template('index.html')

@app.route('/agendar')
def agendar ():
    return render_template('agendar.html')

@app.route('/visualizar')
def visualizar():
    return render_template('visualizar.html')


