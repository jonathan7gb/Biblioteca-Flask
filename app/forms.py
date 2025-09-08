from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import db, bcrypt, app
from app.models import User, Livro, Emprestimo
from datetime import date

import os
from werkzeug.utils import secure_filename

class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    btnCadastrar = SubmitField('Cadastrar')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Usuário já cadastrado com esse Email!")

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        user = User(
            nome = self.nome.data,
            email = self.email.data,
            telefone = self.telefone.data,
            senha = senha
        )
        db.session.add(user)
        db.session.commit()
        return user

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Logar')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, self.senha.data.encode()):
            return user
        return None

class LivroForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    autor = StringField('Autor', validators=[DataRequired()])
    editora = StringField('Editora', validators=[DataRequired()])
    anoPublicacao = IntegerField('Ano de Publicacão', validators=[DataRequired()])
    genero = StringField('Gênero', validators=[DataRequired()])
    quantidade_disponivel = IntegerField('Quantidade Disponível', validators=[DataRequired()])
    status = StringField('Status')
    btnSubmit = SubmitField('Enviar')

    def save(self):
        qtd = self.quantidade_disponivel.data
        status1 = "Indisponível" if qtd <= 0 else "Disponível"
        qtd = self.quantidade_disponivel.data if qtd > 0 else 0
        
        livro = Livro(
            titulo = self.titulo.data,
            autor = self.autor.data,
            editora = self.editora.data,
            anoPublicacao = self.anoPublicacao.data,
            genero = self.genero.data,
            quantidade_disponivel = qtd,
            status = status1
        )
        db.session.add(livro)
        db.session.commit()

class EmprestimoForm(FlaskForm):
    data_emprestimo = DateField('Data do Empréstimo', validators=[DataRequired()])
    data_devolucao = DateField('Data de Devolução', validators=[DataRequired()])
    user_id = SelectField('Usuário', coerce=int, validators=[DataRequired()])
    livro_id = SelectField('Livro', coerce=int, validators=[DataRequired()])
    statusEmprestimo = StringField('Status')
    btnSubmit = SubmitField('Enviar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id.choices = [(u.id, u.nome) for u in User.query.all()]
        self.livro_id.choices = [(l.id, l.titulo) for l in Livro.query.all()]
    
    def save(self):
        hoje = date.today()

        if self.data_devolucao.data < hoje:
            status = "Devolução Atrasada"
        elif self.data_devolucao.data == hoje:
            status = "Entrega Hoje"
        else:
            status = "Dentro do Prazo"

        emprestimo = Emprestimo(
            data_emprestimo=self.data_emprestimo.data,
            data_devolucao=self.data_devolucao.data,
            user_id=self.user_id.data,
            livro_id=self.livro_id.data,
            statusEmprestimo = status
        )

        db.session.add(emprestimo)
        db.session.commit()
