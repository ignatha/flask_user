 # Flask settings
SECRET_KEY = 'your-secret'
ENV = 'development'
DEBUG = True

# Flask-SQLAlchemy settings
# menggunakan SQLITE : sqlite:///app.db
# menggunakan MYSQL : 'mysql+pymysql://user:password@localhost/database'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/database'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# PENTING
# Harap lengkapi konfigurasi smtp untuk mengaktifkan fitur konfirmasi email
MAIL_SERVER = #host smtp
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = #username
MAIL_PASSWORD = #password
MAIL_DEFAULT_SENDER = #alamat pengirim

# Flask-User settings
USER_APP_NAME = "My App"
USER_ENABLE_EMAIL = True
USER_ENABLE_USERNAME = False
USER_EMAIL_SENDER_NAME = USER_APP_NAME
USER_EMAIL_SENDER_EMAIL = "admin@yourapp.com"

#Default Admin
ADMIN_EMAIL = "secret" #Email admin default
ADMIN_PASSWORD = "secret" #password admin default