import os
import secrets
from PIL import Image
from flask_mail import Message
from flaskblog import mail
from flask import url_for, current_app

def save_picture(form_picture):
    randox_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # return name file and extension file
    picture_fn = randox_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # resizing larte pictures
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    print(token)
    msg = Message('Solicitud de cambio de contraseña', 
                    sender='jxexcxo@gmail.com', 
                    recipients=[user.email])
    msg.body = f''' Para cambiar tu contraseña sigue el siguente
                    enlace: {url_for('reset_token', token=token, _external=True)}
                '''
    mail.send(msg)