from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class TodoForm(FlaskForm):
    description = StringField('Descripción', validators=[DataRequired()])
    email = StringField('Correo electrónico')
    company = StringField('Compañía')
    job_title = StringField('Puesto de trabajo')
    client = StringField('Cliente')
    submit = SubmitField('Crear')

class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')

class UpdateTodoForm(FlaskForm):
    submit = SubmitField('Actualizar')
