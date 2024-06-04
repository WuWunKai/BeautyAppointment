from flask import Blueprint, request, jsonify, render_template
from app.models import db, User, Store, UserStoreMembership
from app.line_messaging import send_line_message
from sqlalchemy.exc import SQLAlchemyError
import requests

consumer = Blueprint('consumer', __name__)

@consumer.route('/consumer')
def consumer_index():
    return render_template('consumer/some_consumer_page.html')

@consumer.route('/bind_line', methods=['POST'])
def bind_line():
    data = request.get_json()
    line_user_id = data.get('line_user_id')
    name = data.get('name')
    phone_number = data.get('phone_number')
    email = data.get('email')
    birthday = data.get('birthday')
    store_id = data.get('store_id')

    try:
        with db.session.begin():
            user = User.query.filter_by(line_user_id=line_user_id).first()
            store = Store.query.get(store_id)

            if not store:
                return jsonify({"message": "Store not found!"}), 404

            if not user:
                user = User(
                    line_user_id=line_user_id,
                    name=name,
                    phone_number=phone_number,
                    email=email
                )
                db.session.add(user)
                db.session.flush()  # 獲取自動生成的user.id

            # Check if the membership already exists
            membership = UserStoreMembership.query.filter_by(user_id=user.id, store_id=store.id).first()
            if membership:
                return jsonify({"message": f"親愛的{name}用戶您好，你已經與店家: {store.store_name} 綁定帳號。"}), 400

            new_membership = UserStoreMembership(
                user_id=user.id,
                store_id=store.id,
                birthday=birthday
            )
            db.session.add(new_membership)
            db.session.flush()  # 確保新membership已經寫入數據庫以便後續回滾
            print(line_user_id)
            # 發送LINE消息
            if store.channel_access_token:
                message = f"親愛的{name}您好，你已經與{store.store_name}綁定帳號成功。"
                status_code, response = send_line_message(store.channel_access_token, line_user_id, message)
                if status_code != 200:
                    db.session.rollback()
                    return jsonify({"message": "綁定成功，但發送消息失敗", "error": response}), 200

        return jsonify({"message": f"親愛的{name}您好，你已經與店家: {store.store_name} 綁定帳號成功"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "綁定過程中發生錯誤", "error": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "綁定過程中發生錯誤", "error": str(e)}), 500

@consumer.route('/bind_line_page', methods=['GET'])
def bind_line_page():
    return render_template('consumer/bind_line.html')

