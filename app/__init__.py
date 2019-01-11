import datetime
from flask import Flask, request, render_template_string, redirect, url_for, render_template, jsonify
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import literal_column
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from datatables import ColumnDT, DataTables
from itsdangerous import URLSafeSerializer
from sqlalchemy.ext.hybrid import hybrid_property

 
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
if not User.query.filter(User.email == 'admin@gmail.com').first():
    user = User(
        email='admin@gmail.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password=user_manager.hash_password(app.config['ADMIN_PASSWORD']),
    )
    user.roles.append(Role(name='Admin'))
    db.session.add(user)
    db.session.commit()


# Home bisa diakses tanpa login
@app.route('/')
def home_page():
    return render_template('home.html')

# Halaman user (HANYA ADMIN)
@app.route('/user/')
@login_required
@roles_required('Admin')
def user():
    users = User.query.all()
    return render_template('user/user.html',users=users)

# Halaman user dengan itsdangerous (HANYA ADMIN)
@app.route('/user/detail/<user_id>')
@login_required
@roles_required('Admin')
def user_detail(user_id):
    user_id = danger.loads(user_id)
    return str(user_id)

# Perobcaan serverside DataTables
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


@app.route('/admin')
@roles_required('Admin')
def admin_page():
    return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>{%trans%}Admin Page{%endtrans%}</h2>
                <p><a href={{ url_for('user.register') }}>{%trans%}Register{%endtrans%}</a></p>
                <p><a href={{ url_for('user.login') }}>{%trans%}Sign in{%endtrans%}</a></p>
                <p><a href={{ url_for('home_page') }}>{%trans%}Home Page{%endtrans%}</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>{%trans%}Member Page{%endtrans%}</a> (login_required: member@example.com / Password1)</p>
                <p><a href={{ url_for('admin_page') }}>{%trans%}Admin Page{%endtrans%}</a> (role_required: admin@example.com / Password1')</p>
                <p><a href={{ url_for('user.logout') }}>{%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

@app.route('/login')
def login_page():
    return render_template('login.html')