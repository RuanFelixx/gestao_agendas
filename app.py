from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user
from models import User, Contato
from config import email, senha

# Cara, isso aqui tá uma baita bagunça, já mudei alguns dos link e até apague páginas que tava sendo totalmente inúteis, inclusive ainda tem páginas que tem que ser ajeitadas.
# Oque fazer nesse primeiro momento:
"""
1ª - MySQLdb.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: NO)")
2ª - Vê se as páginas estão "respondendo" aos comandos.
3ª - A página visualizar não tem nada!
4ª - Conferir se tá tudo OK. 
5ª - Apagar essa quantidade absurda de comentários.
"""


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
        conn.execute('SELECT usu_senha FROM tb_usuarios WHERE usu_email=%s', (email,))
        senha_hash = conn.fetchone()
        conn.close()  # Close cursor

        if senha_hash and check_password_hash(senha_hash['usu_senha'], str(senha)):
            login_user(User.get_by_email(email))
            return redirect(url_for('index'))
        else:
            return "Invalid email or password"  
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
        return redirect(url_for('index')) #mudei para index para ir fazer o logi em vez de ja logar assim que faz o cadastro   
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
        # Fazer com base na cateoria
        tar_cat_id = 1 # Esse valor é só um teste
        tar_usu_id = 1 # Esse também

    # OK! Os erros, segundo Romerito, são esses:  
    # Pegar do banco cat_id e user_id
        """Tem que pegar esses dois valores do banco, porque eles são chaves estrangeiras, 
        mas seus valores não estão sendo passados. Além disso, também testamos fazer tar_cat_id = 1 e tar_user_id = 1, só que isso 
        deu ruin, não sei porque. 

        RESOLUÇÃO, SEGUNDO OQUE EU ENTENDI QUE ROMERITO DISSE:
            Pegar os valores de cat_id e user_id do próprio banco e adicionar.
        """
    # tar_cat_id = cat_id
    # tar_user_id = user_id


        conn = conexao.connection.cursor()
        conn.execute("INSERT INTO tb_tarefas (tar_nome, tar_descricao, tar_entrega, tar_cat_id, tar_usu_id) VALUES (%s, %s, %s, %s, %s)", (tar_nome, tar_descricao, tar_entrega, tar_cat_id, tar_usu_id))
        conexao.connection.commit()
        conn.close()  

        return redirect(url_for('index')) 
    # Retornar o form
    """O form não tá sendo retornado, e isso tá dando erro na hora de cadastrar tarefas, porque só presta se tiver tudo OK,
    mas se o usuário cometer qualquer erro o sistema dá erro porque não retorna nada.
    """

# Talvez tenha que mexer aqui também!
@app.route('/agendar')
def agendar():
    return render_template('agendar.html')

# Essa rota só pode ser finalizada quando os banco tiver funcionando, porque aqui é onde vão ser exibidas as tarefas
@app.route('/visualizar')
def visualizar():
    return render_template('visualizar.html')

if __name__ == "__main__":
    app.run(debug=True)
