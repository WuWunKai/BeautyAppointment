# from app import create_app


# app = create_app()


# if __name__ == '__main__':
#     app.run(ssl_context="adhoc")
    
# run.py
import os
from app import create_app, db

app = create_app()
app.secret_key = os.urandom(24) 

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True,ssl_context="adhoc")