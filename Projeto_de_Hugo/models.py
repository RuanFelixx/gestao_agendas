from flask_mysqldb import MySQL
from flask_login import UserMixin
from flask import Flask

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_agenda' 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

conexao = MySQL(app)

class User(UserMixin):
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

    @classmethod
    def get(cls, id):
        conn = conexao.connection.cursor()
        conn.execute('SELECT * FROM tb_usuarios WHERE usu_id=%s', (id,))
        dados = conn.fetchone()
        conn.close()  
        if dados:
            user = User(dados['usu_email'], dados['usu_senha'])
            user.id = dados['usu_id']
            return user
        return None 

    @classmethod
    def get_by_email(cls, email):
        conn = conexao.connection.cursor()
        conn.execute('SELECT * FROM tb_usuarios WHERE usu_email=%s', (email,))
        dados = conn.fetchone()
        conn.close() 
        if dados:    
            user = User(dados['usu_email'], dados['usu_senha'])
            user.id = dados['usu_id']
            return user
        return None 
class Contato:
    def __init__(self,nome,email):
        self.nome = nome
        self.email = email

