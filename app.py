from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
from models import User, Contato
from flask_mail import Mail, Message
from config import email, senha


app = Flask(__name__)
app.secret_key = 'sebosao'

email_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USER_TLS": False,
    "MAIL_USER_SSL": True,
    "MAIL_USERNAME": email,
    "MAIL_PASSWORD": senha
}


app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "projetoro"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config.update(email_settings)

mail = Mail(app)
conexao = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def inicial():
    return render_template('inicial.html')

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

        formcontato = Contato(nome,email)

        msg = Message(
            subject= f'{formcontato.nome} obrigado por se cadastrar nop nosso site',
            sender = app.config.get("MAIL_USERNAME"),
            recipients = [formcontato.email, app.config.get("MAIL_USERNAME")],
            body = ''' 
            
            {formcontato.nome} você fez login com o email {fromcontato.email}, obrigado por fazer
            parte da nossa historia !!

            '''
        )

        mail.send(msg)
        flash('email enviado com sucesso!')

        if senha_hash and check_password_hash(senha_hash['usu_senha'], str(senha)):
            login_user(User.get_by_email(email))
            return redirect(url_for('inicial'))
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

        formcontato = Contato(nome,email)

        msg = Message(
            subject= f'{formcontato.nome} obrigado por se cadastrar nop nosso site',
            sender = app.config.get("MAIL_USERNAME"),
            recipients = [formcontato.email, app.config.get("MAIL_USERNAME")],
            body = ''' 
            
            {formcontato.nome} você se cadastrou com o email {fromcontato.email}, obrigado por fazer
            parte da nossa historia !!

            '''
        )

        mail.send(msg)
        flash('email enviado com sucesso!')

        login_user(User.get_by_email(email))
        return redirect(url_for('inicial')) #mudei para inicia'l para ir fazer o logi em vez de ja logar assim que faz o cadastro   
    return render_template('cadastro.html')


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


# apagadas as rotas /agendar e /visualizar pois elas não estao sendo usadas


if __name__ == "__main__":
    app.run(debug=True)


