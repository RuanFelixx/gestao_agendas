from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import User, Contato
from config import email, senha
from datetime import datetime


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
        email = request.form['email']
        senha = request.form['senha']
        conn = conexao.connection.cursor()
        conn.execute('SELECT usu_senha FROM tb_usuarios WHERE usu_email=%s', (email,))
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
        tar_status = request.form['status']
        data_criacao = datetime.now()

        conn = conexao.connection.cursor()
        categoria = request.form['cat_nome']
        cat = conn.execute('SELECT cat_id FROM tb_categoria_tarefas WHERE cat_nome = %s',(categoria,))
        if not cat:
            conn.execute('INSERT INTO tb_categoria_tarefas(cat_nome) VALUES(%s)',(categoria,))
            cat = conn.execute('SELECT cat_id FROM tb_categoria_tarefas WHERE cat_nome = %s',(categoria,))
            render_template('index.html')
        tar_cat_id = cat
        tar_usu_id = current_user.id

        conn.execute("INSERT INTO tb_tarefas (tar_nome, tar_descricao, tar_entrega, tar_datacriacao, tar_cat, tar_status, tar_prioridade, tar_usu_id, tar_cat_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (tar_nome, tar_descricao, tar_entrega, data_criacao, categoria,tar_status, tar_prioridade, tar_usu_id, tar_cat_id,))
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
    conn.execute('SELECT * FROM tb_tarefas JOIN tb_categoria_tarefas ON tar_cat_id = cat_id WHERE tar_usu_id = %s', (usuarioativo,))
    tarefas = conn.fetchall()
    return render_template('visualizar.html', tarefas=tarefas)


@app.route('/filtrar', methods=['POST'])
def filtrar():
    if request.method == 'POST':
        status = request.form.get('status')
        prioridade = request.form.get('prioridade')
        categoria = request.form.get('categoria') or None
        data_limite = request.form.get('data-limite') or None
        data_criacao = request.form.get('data-criacao') or None

        conn = conexao.connection.cursor()

            # Query base
        query = "SELECT * FROM tb_tarefas WHERE tar_usu_id = %s"
        params = [current_user.id] #lista com os parametros

            # Condições opcionais
        if status: #se tiver sido passado algum status
            query += " AND tar_status = %s" #adiciona à query
            params.append(status) #adiciona o parametro a lista de parâmetros
        if prioridade:
            query += " AND tar_prioridade = %s"
            params.append(prioridade)
        if categoria:
            if categoria == '1':
                params.append('Compromisso')
            elif categoria == '2':
                params.append('Trabalho')
            elif categoria == '3':
                params.append('Atividades')
            query += " AND tar_cat= %s"
        if data_limite:
            query += " AND tar_data_limite = %s"
            params.append(data_limite)
        if data_criacao:
            query += " AND tar_data = %s"
            params.append(data_criacao)

        conn.execute(query, params)
        tarefas = conn.fetchall()
        conn.close()
        return render_template('visualizar.html',tarefas=tarefas)



@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')

@app.route('/deletar/<int:id>') 
def deletar(id):
    conn = conexao.connection.cursor()
    conn.execute('DELETE FROM tb_tarefas WHERE tar_id=%s',(id,))
    conexao.connection.commit()
    conn.close()  

    return redirect(url_for('visualizar'))

@app.route('/editar/<int:id>', methods=['POST','GET'])
def editar(id):
    conn = conexao.connection.cursor()
    if request.method == 'GET':
        conn.execute('SELECT * FROM tb_tarefas WHERE tar_id=%s',(id,))
        tarefa = conn.fetchone()
        return render_template('editar.html', tarefa=tarefa)
    else:
        tar_nome = request.form['nome_atividade']
        tar_descricao = request.form['desc_atividade']
        tar_entrega = request.form['data_da_atividade']
        tar_prioridade = request.form['prioridade']
        tar_status = request.form['status']
        tar_categoria = request.form['cat_nome']
        conn.execute('''UPDATE tb_tarefas SET tar_nome=%s,tar_descricao=%s,tar_entrega=%s,
                     tar_prioridade=%s, tar_status=%s, tar_cat=%s WHERE tar_id=%s''', (tar_nome,tar_descricao,tar_entrega,tar_prioridade,tar_status,tar_categoria, id))
        conexao.connection.commit()
        conn.close()
        return redirect(url_for('visualizar'))


if __name__ == "__main__":
    app.run(debug=True)
