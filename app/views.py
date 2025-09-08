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

@app.route('/usuarios/delete/<int:id>', methods=['POST'])
@login_required
def delete_usuario(id):
    usuarios = User.query.get_or_404(id)

    db.session.delete(usuarios)
    db.session.commit()
    
    return redirect(url_for('usuarios')) 

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

@app.route('/livros/delete/<int:id>', methods=['POST'])
@login_required
def delete_livro(id):
    livro = Livro.query.get_or_404(id)

    db.session.delete(livro)
    db.session.commit()
    
    return redirect(url_for('livros')) 

@app.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_livro(id):
    livro = Livro.query.get_or_404(id)
    form = LivroForm(obj=livro)

    if form.validate_on_submit():
        form.populate_obj(livro)
        db.session.commit()
        return redirect(url_for('livros'))

    return render_template('editar_livro.html', form=form, livro=livro)

@app.route('/emprestimos/')
@login_required
def emprestimos():
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados = Emprestimo.query.join(User).order_by(Emprestimo.id)
    
    if pesquisa != '':
        dados = dados.join(Emprestimo.livro).filter(Livro.titulo.ilike(f'%{pesquisa}%'))
    
    emprestimos = {'dados' : dados.all()}
    return render_template('emprestimos.html', emprestimos=emprestimos)

@app.route('/cadastroemprestimo/', methods=['GET', 'POST'])
@login_required
def emprestimo_cadastro():
    form = EmprestimoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('emprestimos'))
    return render_template('cadastro_emprestimo.html', context=context, form=form)

@app.route('/emprestimos/delete/<int:id>', methods=['POST'])
@login_required
def delete_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)

    db.session.delete(emprestimo)
    db.session.commit()
    
    return redirect(url_for('emprestimos')) 

@app.route('/emprestimos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    form = EmprestimoForm(obj=emprestimo)

    if form.validate_on_submit():
        form.populate_obj(emprestimo)
        db.session.commit()
        return redirect(url_for('emprestimos'))

    return render_template('editar_emprestimo.html', form=form, emprestimo=emprestimo)