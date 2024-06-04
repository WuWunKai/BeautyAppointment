from flask import Blueprint, jsonify, request
from app.models import db, Store, UserStoreMembership, User

store = Blueprint('store', __name__)

@store.route('/get_store_name', methods=['GET'])
def get_store_name():
    store_id = request.args.get('store_id')
    store = Store.query.get(store_id)
    
    if not store:
        return jsonify({"message": "找不到該店家"}), 404

    return jsonify({
        "store_name": store.store_name,
        "liff_id": store.liff_id  # 返回 liff_id
    }), 200

@store.route('/check_binding', methods=['GET'])
def check_binding():
    line_user_id = request.args.get('user_id')
    store_id = request.args.get('store_id')
    
    user = User.query.filter_by(line_user_id=line_user_id).first()

    if user:
        membership = UserStoreMembership.query.filter_by(user_id=user.id, store_id=store_id).first()
        if membership:
            return jsonify({
                "is_bound": True,
                "phone_number": user.phone_number,
                "email": user.email,
                "birthday": membership.birthday.strftime('%Y-%m-%d') if membership.birthday else ''
            }), 200

    return jsonify({"is_bound": False}), 200