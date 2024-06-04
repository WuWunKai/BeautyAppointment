# create_db.py

from app import create_app, db
from app.models import User, Store, Service, Appointment, Order, Staff, ConsumerManagement, Calendar

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created")