 # Flask settings
SECRET_KEY = 'your-secret'
ENV = 'development'
DEBUG = True

# Flask-SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/database'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# Flask-Mail SMTP server settings
MAIL_SERVER = 
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = 
MAIL_PASSWORD = 
MAIL_DEFAULT_SENDER = 

# Flask-User settings
USER_APP_NAME = "My App" # Shown in and email templates and page footers
USER_ENABLE_EMAIL = True        # Enable email authentication
USER_ENABLE_USERNAME = False    # Disable username authentication
USER_EMAIL_SENDER_NAME = USER_APP_NAME
USER_EMAIL_SENDER_EMAIL = "admin@yourapp.com"

#Default Admin Password
ADMIN_PASSWORD = "secret"