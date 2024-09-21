from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "tarefas"
app.config["MYSQL_DB"] = "projetoro"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

conexao = MySQL(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        tar_nome = request.form['tar_nome']
        tar_descricao = request.form['tar_descricao']
        tar_entrega = request.form['tar_entrega']

        conn = conexao.connection.cursor()
        conn.execute("""
            INSERT INTO tb_tarefas (tar_nome, tar_descricao, tar_entrega) 
            VALUES (%s, %s, %s)
        """, (tar_nome, tar_descricao, tar_entrega))
        conexao.connection.commit()
        conn.close()

        return render_template('form.html', nome_da_atividade=tar_nome)

@app.route('/inicial', methods=['GET', 'POST'])
def inicial():
    return render_template('inicial.html')

@app.route('/agendar')
def agendar ():
    return render_template('agendar.html')

@app.route('/visualizar')
def visualizar():
    return render_template('visualizar.html')

if __name__ == "__main__":
    app.run(debug=True)



