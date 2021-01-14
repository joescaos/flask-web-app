import secrets
import os
from PIL import Image
from flask import render_template, redirect, url_for, flash, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
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

def save_picture(form_picture):
    randox_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # return name file and extension file
    picture_fn = randox_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resizing larte pictures
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data 
        db.session.commit()
        flash('Tu cuenta fue actualizada', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        app.logger.debug(current_user.username, current_user.email)
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Cuenta personal', 
                                        image_file=image_file, form=form)

