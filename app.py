from flask import Flask, render_template, request, redirect, url_for
import database as db

app = Flask(__name__)

@app.route('/')
def index():
    """
    Rota principal. Lista todas as tarefas.
    """
    tarefas = db.listar_todas_tarefas()
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    """
    Rota para adicionar uma nova tarefa.
    Processa os dados do formulário da página inicial.
    """
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        
        if titulo and descricao:
            db.criar_tarefa(titulo, descricao)
    
    return redirect(url_for('index'))

@app.route('/editar/<id_tarefa>', methods=['GET', 'POST'])
def editar(id_tarefa):
    """
    Rota para editar uma tarefa.
    GET: Mostra o formulário de edição com os dados da tarefa.
    POST: Atualiza os dados da tarefa no banco.
    """
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        status = request.form['status']
        
        dados_atualizacao = {
            'titulo': titulo,
            'descricao': descricao,
            'status': status
        }
        
        db.atualizar_tarefa(id_tarefa, dados_atualizacao)
        return redirect(url_for('index'))

    
    tarefa = db.obter_tarefa(id_tarefa)
    if tarefa:
        return render_template('editar.html', tarefa=tarefa)
    else:
        
        return redirect(url_for('index'))

@app.route('/deletar/<id_tarefa>', methods=['POST'])
def deletar(id_tarefa):
    """
    Rota para deletar uma tarefa.
    """
    db.deletar_tarefa(id_tarefa)
    return redirect(url_for('index'))

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)