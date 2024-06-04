from . import db

class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(100), nullable=False)
    ig = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    tiktok = db.Column(db.String(100))
    description = db.Column(db.Text)
    channel_id = db.Column(db.String(100))  
    channel_secret = db.Column(db.String(100))  
    channel_access_token = db.Column(db.String(255))  
    liff_id = db.Column(db.String(50)) 
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    line_user_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class UserStoreMembership(db.Model):
    __tablename__ = 'user_store_memberships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    birthday = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('memberships', lazy=True))
    store = db.relationship('Store', backref=db.backref('memberships', lazy=True))
    
class ServiceCategory(db.Model):
    __tablename__ = 'service_categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False, comment='分類名稱')

    services = db.relationship('Service', backref='category', lazy=True)

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False, comment='店家ID')
    service_name = db.Column(db.String(100), nullable=False, comment='服務名稱')
    duration = db.Column(db.Integer, nullable=False, comment='時長（分鐘）')
    price = db.Column(db.Numeric(10, 2), nullable=False, comment='價格')
    display_price = db.Column(db.Boolean, default=True, nullable=False, comment='顯示價格')
    description_toggle = db.Column(db.Boolean, default=True, nullable=False, comment='服務介紹開關')
    description = db.Column(db.Text, comment='服務介紹')
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False, comment='分類ID')
    image_url1 = db.Column(db.String(255), comment='服務照片1')
    image_url2 = db.Column(db.String(255), comment='服務照片2')
    image_url3 = db.Column(db.String(255), comment='服務照片3')
    image_url4 = db.Column(db.String(255), comment='服務照片4')
    image_url5 = db.Column(db.String(255), comment='服務照片5')
    selection_type = db.Column(db.Enum('單選', '複選', name='selection_type'), nullable=False, comment='子服務選擇類型')

    sub_services = db.relationship('SubService', backref='service', lazy=True)

class SubService(db.Model):
    __tablename__ = 'sub_services'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False, comment='服務ID')
    sub_service_name = db.Column(db.String(100), nullable=False, comment='子服務名稱')
    sub_service_duration = db.Column(db.Integer, nullable=False, comment='子服務時長（分鐘）')
    sub_service_price = db.Column(db.Numeric(10, 2), nullable=False, comment='子服務價格')
    sub_service_order = db.Column(db.Integer, nullable=False, comment='子服務排序')