from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user
from models import User, Contato
from config import email, senha

app = Flask(__name__)
app.secret_key = 'sebosao'

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "db_agenda"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

conexao = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        conn = conexao.connection.cursor()
        conn.execute('SELECT usu_senha FROM tb_usuarios WHERE usu_email=%s and usu_nome=%s', (email, nome))
        senha_hash = conn.fetchone()
        conn.close()  # Close cursor
        

        if senha_hash and check_password_hash(senha_hash['usu_senha'], str(senha)):
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
          
    return render_template('login.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])

        conn = conexao.connection.cursor()
        conn.execute('INSERT INTO tb_usuarios(usu_nome, usu_senha, usu_email) VALUES (%s, %s, %s)', (nome, senha, email))
        conexao.connection.commit()
        conn.close() 

        login_user(User.get_by_email(email))
        return redirect(url_for('index'))  
    return render_template('cadastro.html')


login_manager = LoginManager()
app.config['SECRET_KEY'] = 'tarefas'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        tar_nome = request.form['nome_atividade']
        tar_descricao = request.form['desc_atividade']
        tar_entrega = request.form['data_da_atividade']
        
        conn = conexao.connection.cursor()
        conn.execute("INSERT INTO tb_tarefas (tar_nome, tar_descricao, tar_entrega, tar_cat_id, tar_usu_id) VALUES (%s, %s, %s, %s, %s)", (tar_nome, tar_descricao, tar_entrega, tar_cat_id, tar_usu_id))
        conexao.connection.commit()
        conn.close()  

        return redirect(url_for('index')) 

@app.route('/agendar')
def agendar():
    return render_template('agendar.html')

@app.route('/visualizar')
def visualizar():
    conn = conexao.connection.cursor()
    conn.execute("SELECT * FROM tb_tarefas")
    tarefas = conn.fetchall()
    conn.close()
    return render_template('visualizar.html', tarefas=tarefas)

if __name__ == "__main__":
    app.run(debug=True)
