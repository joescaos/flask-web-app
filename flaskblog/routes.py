from flask import render_template, redirect, url_for, flash, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Johan Esteban',
        'title': 'Primer post',
        'content': 'Este es el primer post de esta app',
        'date_posted': 'Enero 12, 2021'
    },
    {
        'author': 'Jhon Doe',
        'title': 'Segundo post',
        'content': 'Este es el segundo post de esta app',
        'date_posted': 'Enero 12, 2021'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # decode for instead bytes have string
        user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Cuenta creada ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        #if form.email.data == 'jxexcxo@gmail.com' and form.password.data == 'password':
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Inicio de sesión exitosa', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Inicio de sesión fallida verifica tus datos', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Cuenta personal')