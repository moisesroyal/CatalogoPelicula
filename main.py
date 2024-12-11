import unittest
from flask import Flask, render_template, redirect, url_for, flash, request, make_response, session, jsonify
from flask_login import login_required, current_user, login_user
from app import create_app
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm, LoginForm
from app.firestore_service import update_todo, get_todos, put_todo, delete_todo
from google.cloud import firestore
import os
from app.models import UserModel

app = Flask(__name__)
app = create_app()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/root/Pelicula/moises-proyecto-flask-73105f19c9e0.json"
db = firestore.Client()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response

@app.route('/index')
def index_page():
    return render_template('index.html')

@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form
    }

    if todo_form.validate_on_submit():
        put_todo(
            user_id=username,
            description=todo_form.description.data,
            email=todo_form.email.data or '',
            company=todo_form.company.data or '',
            job_title=todo_form.job_title.data or '',
            client=todo_form.client.data or ''
        )

        flash('Tu tarea se creo con exito!')
        return redirect(url_for('hello'))

    return render_template('hello.html', **context)

@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>', methods=['GET', 'POST'])
@login_required
def update(todo_id):
    user_id = current_user.id
    update_form = UpdateTodoForm()

    if request.method == 'POST' and update_form.validate_on_submit():
        description = request.form['description']
        email = request.form['email']
        company = request.form['company']
        job_title = request.form['job_title']
        client = request.form['client']

        update_todo(
            user_id=user_id,
            todo_id=todo_id,
            description=description,
            email=email,
            company=company,
            job_title=job_title,
            client=client,
        )
        flash('Tarea actualizada con exito.')
        return redirect(url_for('hello'))

    todos = get_todos(user_id=user_id)
    todo = next((t for t in todos if t.id == todo_id), None)
    if todo:
        return render_template('edit_todo.html', todo=todo, update_form=update_form)
    else:
        flash('Tarea no encontrada.')
        return redirect(url_for('hello'))

@app.route('/tasks')
@login_required
def tasks():
    username = current_user.id
    todos = get_todos(user_id=username)
    return render_template('tasks_utf8.html', tasks=todos)


@app.route('/api/data', methods=['POST'])
def handle_data_post():
    data = request.json

    if not data:
        return jsonify({"message": "No se recibieron datos."}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Usuario o contraseña faltantes."}), 400

    save_user_data(username, password)

    response = {
        "message": "Datos procesados correctamente",
        "received_data": data
    }
    return jsonify(response)

def save_user_data(username, password):
    doc_ref = db.collection('users').document(username)
    doc_ref.set({
        'username': username,
        'password': password
    })
    print(f"Datos guardados para el usuario {username} en Firestore.")
    
@app.route('/catalogo/<categoria>')
def catalogo(categoria):
    return render_template('catalogo.html', categoria=categoria)

if __name__ == '__main__':
    app.run(debug=True)
    



    
