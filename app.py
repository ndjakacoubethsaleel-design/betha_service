from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'betha2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///betha.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ndjakacoubethsaleel@gmail.com'
app.config['MAIL_PASSWORD'] = 'nttulblnzarsvvvw'

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'connexion'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    mot_de_passe = db.Column(db.String(200))
    verifie = db.Column(db.Boolean, default=False)
    en_ligne = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        mdp = generate_password_hash(request.form['mot_de_passe'])
        code = str(random.randint(100000, 999999))
        session['code'] = code
        session['nom'] = nom
        session['email'] = email
        session['mdp'] = mdp
        try:
            msg = Message('Code de vérification BETHA-SERVICE',
                          sender='ndjakacoubethsaleel@gmail.com',
                          recipients=[email])
            msg.body = f'Bonjour {nom},\n\nVotre code de vérification est : {code}\n\nBETHA-SERVICE'
            mail.send(msg)
        except Exception as e:
            print(f"Erreur email: {e}")
        return redirect(url_for('verifier'))
    return render_template('inscription.html')

@app.route('/verifier', methods=['GET', 'POST'])
def verifier():
    if request.method == 'POST':
        code_entre = request.form['code'].strip()
        code_session = session.get('code', '')
        if code_entre == code_session:
            user = User(nom=session['nom'], email=session['email'],
                       mot_de_passe=session['mdp'], verifie=True)
