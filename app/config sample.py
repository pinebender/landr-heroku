import os

#CSRF Enable
CSRF_ENABLED = True

#temporary dev key; note that it is CAPS in config file; from app.py it would be app.secret_key. 
SECRET_KEY = 'DEV_KEY' 

#sqlalchemy database config
SQLALCHEMY_DATABASE_URI = "postgresql://user:pass@localhost/db"

