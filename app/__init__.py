import datetime
from flask import Flask, request, render_template_string, redirect, url_for, render_template, jsonify
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import literal_column
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from datatables import ColumnDT, DataTables
from itsdangerous import URLSafeSerializer
from sqlalchemy.ext.hybrid import hybrid_property
import base64

 
app = Flask(__name__)
app.config.from_object('config')
danger = URLSafeSerializer(app.config['SECRET_KEY'])


babel = Babel(app)
db = SQLAlchemy(app)

# Model User
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')


    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    roles = db.relationship('Role', secondary='user_roles')

    # mehod itsdangerous
    @hybrid_property
    def danger(self):
        return danger.dumps(self.id)

# Model Role
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Snippet User relation Role
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Flask_user custom
class CustomUserManager(UserManager):

    # Custom Method register View
    def register_view(self):
        # Redirect ke home jika sudah login
        if self.call_or_get(current_user.is_authenticated) and self.USER_AUTO_LOGIN_AT_LOGIN:
            return redirect(url_for('home_page'))
        
        return super(CustomUserManager, self).register_view()

# Setup Flask-User
user_manager = CustomUserManager(app, db, User)

# Membangun database
db.create_all()

# Membuat user admin default
if not User.query.filter(User.email == app.config['ADMIN_EMAIL']).first():
    user = User(
        email=app.config['ADMIN_PASSWORD'],
        email_confirmed_at=datetime.datetime.utcnow(),
        password=user_manager.hash_password(app.config['ADMIN_PASSWORD']),
    )
    user.roles.append(Role(name='Admin'))
    db.session.add(user)
    db.session.commit()


# Home bisa diakses tanpa login
@app.route('/')
@login_required
def home_page():
    return render_template('home.html')

# Halaman user (HANYA ADMIN)
@app.route('/user/')
@login_required
def user():
    users = User.query.all()
    return render_template('user/user.html',users=users,page_title="Users",page_description="List Of Table User")

# Halaman user dengan itsdangerous (HANYA ADMIN)
@app.route('/user/detail/<user_id>')
@login_required
def user_detail(user_id):
    user_id = danger.loads(user_id)
    user = User.query.get(user_id)
    return render_template('user/profile.html',user=user)


@app.route('/gambar/',methods=['GET','POST'])
@login_required
def gambar():
    if request.method == 'GET':
        return render_template('gambar/index.html',page_title="Konversi Gambar",page_description="Konversi file gambar ke Base64 String")
    if request.method == 'POST':
        image = request.files['gambar']
        image_string = base64.b64encode(image.read())
        data = {}
        data['data'] = image_string
        return jsonify(data)


# Perobcaan API serverside DataTables
@app.route('/API/user')
@login_required
def api_user():

    columns = [
        ColumnDT(User.first_name),
        ColumnDT(User.last_name),
        ColumnDT(User.email),
        ColumnDT(Role.name),
        ColumnDT(User.danger,public_order=False),
    ]

    query = db.session.query()\
                .select_from(User)\
                .outerjoin(User.roles)\

    rowTable = DataTables(request.args.to_dict(),query, columns)

    response = jsonify(rowTable.output_result())
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response