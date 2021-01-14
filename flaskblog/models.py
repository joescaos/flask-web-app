from datetime import datetime
from flaskblog import db
from flaskblog import login_manager
from flask_login import UserMixin

@login_manager.user_loader # decorator para validar si el usuario está autenticado
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), unique=True, nullable=False)
    email= db.Column(db.String(100), unique=True, nullable=False)
    image_file= db.Column(db.String(50), nullable=False, default='default.jpg')
    password= db.Column(db.String(60), nullable=False)
    '''Relacion uno a muchos '''
    # un usuario puede ser autor de uno o muchos posts
    # db.relationship describe la relacion entre el usuario y el post
    # tiene tres params 1: nombre de la clase con la que se establece la relacion}
    # 2: backref con la cual se establece la forma de la relacion el usuario sera el autor del post
    # 3: lazy la forma en que se cargan los datos
    post = db.relationship('Post', backref='author', lazy=True) 

    def __repr__(self):
        return f"User( '{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(100), nullable=False)
    date_posted= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    '''se establece la relacion de el post con el usuario con su id'''
    # una columna de tipo integer params
    # 1: la llave foranea user.id
    # 2: no puede estar vacia
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post( '{self.title}', '{self.date_posted}')"