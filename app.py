from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import User, Contato
from config import email, senha


app = Flask(__name__)


login_manager = LoginManager()
app.config['SECRET_KEY'] = 'tarefas'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "db_agenda"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


conexao = MySQL(app)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

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
        conn.close()

        if senha_hash and check_password_hash(senha_hash['usu_senha'], str(senha)):
            login_user(User.get_by_email(email))
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


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        tar_nome = request.form['nome_atividade']
        tar_descricao = request.form['desc_atividade']
        tar_entrega = request.form['data_da_atividade']
        tar_prioridade = request.form['prioridade']
        conn = conexao.connection.cursor()
        categoria = request.form['cat_nome']
        cat = conn.execute('SELECT cat_id FROM tb_categoria_tarefas WHERE cat_nome = %s',(categoria))
        if not cat:
            conn.execute('INSERT INTO tb_categoria_tarefas(cat_nome) VALUES(%s)',(categoria))
            cat = conn.execute('SELECT cat_id FROM tb_categoria_tarefas WHERE cat_nome = %s',(categoria))
            render_template('index.html')
        tar_cat_id = cat
        tar_usu_id = current_user.id

        conn.execute("INSERT INTO tb_tarefas (tar_nome, tar_descricao, tar_entrega, tar_cat_id, tar_prioridade, tar_usu_id) VALUES (%s, %s, %s, %s, %s, %s)", (tar_nome, tar_descricao, tar_entrega, tar_cat_id, tar_prioridade, tar_usu_id))
        conexao.connection.commit()
        conn.close()  

        return redirect(url_for('index')) 


@app.route('/agendar')
@login_required
def agendar():
    if current_user:
        return render_template('agendar.html')
    else:
        flash('Usuario não autenticado')


@app.route('/visualizar')
def visualizar():
    usuarioativo = current_user.id
    conn = conexao.connection.cursor()
    conn.execute('SELECT * FROM tb_tarefas WHERE tar_usu_id = %s', (usuarioativo,))
    tarefas = conn.fetchall()
    return render_template('visualizar.html', tarefas=tarefas)

if __name__ == "__main__":
    app.run(debug=True)
