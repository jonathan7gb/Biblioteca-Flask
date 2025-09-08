from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=True)
    telefone = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    senha = db.Column(db.String(100), nullable=True)

     # relacionamento com Emprestimo
    emprestimos = db.relationship('Emprestimo', backref='user', lazy=True)

class Livro(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=True)
    autor = db.Column(db.String(100), nullable=True)
    editora = db.Column(db.String(100), nullable=True)
    anoPublicacao = db.Column(db.Integer, nullable=True)
    genero = db.Column(db.String(100), nullable=True)
    quantidade_disponivel = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(100), nullable=True)

    # relacionamento com Emprestimo
    emprestimos = db.relationship('Emprestimo', backref='livro', lazy=True)

class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_emprestimo = db.Column(db.DateTime, default=datetime.now)
    data_devolucao = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_emprestimo_user"), nullable=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id', name="fk_emprestimo_livro"), nullable=True)
    statusEmprestimo = db.Column(db.String(100), nullable=True)
