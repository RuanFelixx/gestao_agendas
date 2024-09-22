from flask_mysqldb import MySQL
from flask_login import UserMixin
from flask import Flask

app = Flask(_name_)

conexao = MySQL(app)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tarefas'
app.config['MYSQL_DB'] = 'db_agenda' 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

conexao = MySQL(app)

class User(UserMixin):
    id : str
    def _init_(self, email, senha):
        self.email = email
        self.senha = senha
        
    @classmethod
    def get(cls, id):
        conn = conexao.connection.cursor()
        dados = conn.execute('SELECT * FROM tb_usuarios WHERE usu_id=%s', (id,))
        dados = conn.fetchone()
        if dados:
            user = User(dados['usu_email'], dados['usu_senha'])
            user.id = dados['usu_id']
            return user

    @classmethod
    def get_by_email(cls, email):
        conn = conexao.connection.cursor()
        dados = conn.execute('SELECT * FROM tb_usuarios WHERE usu_email=%s', (email,))
        dados = conn.fetchone()
        if dados:    
            user = User(dados['usu_email'], dados['usu_senha'])
            user.id = dados['usu_id']
            return user
        return None
