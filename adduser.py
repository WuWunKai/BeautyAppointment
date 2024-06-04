# add_users.py

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # 確保數據庫已經創建
    db.create_all()

    # 新增用戶數據
    user1 = User(UserName='Alice', UserPhone='1234567890', UserEmail='alice@example.com', LineID='alice_line')
    user2 = User(UserName='Bob', UserPhone='0987654321', UserEmail='bob@example.com', LineID='bob_line')
    
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    print("Users added to the database.")