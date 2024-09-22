from flask import Flask, render_template, url_for, redirect, request
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
from user_models import User

app = Flask(__name__)

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "projetoro"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

conexao = MySQL(app)

@app.route('/', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conn = conexao.connection.cursor()
        conn.execute('SELECT usu_senha FROM tb_usuarios WHERE usu_email=%s', (email,))
        senha_hash = conn.fetchone()
        conn.close()  # Close cursor

        if senha_hash and check_password_hash(senha_hash['usu_senha'], str(senha)):
            login_user(User.get_by_email(email))
            return redirect(url_for('inicial'))
        else:
            return "Invalid email or password"  
    return render_template('login.html')

@app.route('/cadastro', methods=['POST'])
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


login_manager = LoginManager()
app.config['SECRET_KEY'] = 'tarefas'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        tar_nome = request.form['tar_nome']
        tar_descricao = request.form['tar_descricao']
        tar_entrega = request.form['tar_entrega']

        try:
            conn = conexao.connection.cursor()
            conn.execute("""
                INSERT INTO tb_tarefas (tar_nome, tar_descricao, tar_entrega) 
                VALUES (%s, %s, %s)
            """, (tar_nome, tar_descricao, tar_entrega))
            conexao.connection.commit()
            conn.close()  

            return redirect(url_for('index')) 
        except Exception as erro:
            return str(erro) 

@app.route('/inicial', methods=['GET', 'POST'])
def inicial():
    return render_template('inicial.html')

@app.route('/agendar')
def agendar():
    return render_template('agendar.html')

@app.route('/visualizar')
def visualizar():
    return render_template('visualizar.html')

if __name__ == "__main__":
    app.run(debug=True)


