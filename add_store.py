import os
from app import create_app, db
from app.models import Store

# 配置環境變量
os.environ['FLASK_APP'] = 'run.py'
os.environ['FLASK_ENV'] = 'development'
os.environ['DATABASE_URL'] = 'mysql+pymysql://root:Lovelena0220&@localhost/BeautyAppointmentSystem'

# 創建Flask應用
app = create_app()

# 使用Flask應用的上下文
with app.app_context():
    # 新增一家店家
    new_store = Store(
        store_name='New Store',
        ig='https://www.instagram.com/newstore',
        facebook='https://www.facebook.com/newstore',
        tiktok='https://www.tiktok.com/@newstore',
        description='This is a new store.'
    )
    
    db.session.add(new_store)
    db.session.commit()
    print(f"Store '{new_store.store_name}' added successfully!")