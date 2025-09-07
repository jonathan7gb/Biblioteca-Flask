from app import app, db
from flask import render_template, url_for, request, redirect
from app.forms import UserForm, LoginForm, EmprestimoForm, LivroForm
from app.models import User, Emprestimo, Livro
from app import bcrypt
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
def homepage():
    form = LoginForm()

    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        if user:
            login_user(user, remember=True)
            return redirect(url_for('homepage'))
        else:
            return render_template('login_user.html', form=form, erro="Usuário ou senha incorretos.")
    return render_template('login_user.html', form=form)

@app.route('/registeruser/', methods=['GET', 'POST'])
def registeruser():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro_user.html', form=form)

@app.route('/sair/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/usuarios/')
@login_required
def usuarios():
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados = User.query.order_by('nome')
    
    if pesquisa != '':
        dados = dados.filter(User.nome.ilike(f'%{pesquisa}%'))
    
    usuarios = {'dados' : dados.all()}
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/livros/')
@login_required
def livros():
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados = Livro.query.order_by('genero')
    
    if pesquisa != '':
        dados = dados.filter(Livro.titulo.ilike(f'%{pesquisa}%'))
    
    livros = {'dados' : dados.all()}
    return render_template('livros.html', livros=livros)

@app.route('/cadastrolivro/', methods=['GET', 'POST'])
@login_required
def livro_cadastro():
    form = LivroForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('livros'))
    return render_template('cadastro_livro.html', context=context, form=form)