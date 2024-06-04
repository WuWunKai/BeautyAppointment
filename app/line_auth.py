# app/line_auth.py

import os
import json
import requests
from flask import Blueprint, request, redirect, url_for, session,flash
from app.models import db, User
from datetime import datetime, timedelta
import pytz
import secrets
from functools import wraps

line_auth = Blueprint('line_auth', __name__)

LINE_CHANNEL_ID = '2005333304'
LINE_CHANNEL_SECRET = '626d40297e44c809ee21ecc194f0c48e'
LINE_REDIRECT_URI = 'https://8173-59-126-46-117.ngrok-free.app/callback'

@line_auth.route('/login/line')
def login_line():
    state = secrets.token_urlsafe(16)
    role = request.args.get('role')
    session['state'] = state
    session['role'] = role
    return redirect(f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={LINE_CHANNEL_ID}&redirect_uri={LINE_REDIRECT_URI}&state={state}&scope=profile%20openid%20email")

@line_auth.route('/callback')
def callback():
    code = request.args.get('code')
    state = session.get('state')
    role = session.get('role')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': LINE_REDIRECT_URI,
        'client_id': LINE_CHANNEL_ID,
        'client_secret': LINE_CHANNEL_SECRET
    }
    response = requests.post('https://api.line.me/oauth2/v2.1/token', headers=headers, data=payload)
    access_token = response.json().get('access_token')
    expires_in = response.json().get('expires_in')  # 有效期秒數
    id_token = response.json().get('id_token')

    response = requests.get('https://api.line.me/v2/profile', headers={'Authorization': f'Bearer {access_token}'})
    profile = response.json()

    print(access_token,id_token,profile)
    # return f"access_token,{access_token} \n id_token,{id_token} \n profile, {profile}!"
    user = User.query.filter_by(LineID=profile.get('userId')).first()
    if user is None:
        user = User(UserName=profile.get('displayName'), LineID= profile.get('userId'))
        db.session.add(user)
        db.session.commit()
    # 存儲 access_token 及其過期時間
    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    session['access_token'] = access_token
    session['token_expiry'] = (utc_now + timedelta(seconds=expires_in)).isoformat()
    session['displayName'] = profile.get('displayName')
    session['userId'] = profile.get('userId')
    # Here we can differentiate based on state
    print(user.UserPhone)
    if role == 'consumer':
        if user.UserPhone == '':
            return redirect(url_for('consumer.edit_user_info'))
        else:
            return redirect(url_for('consumer.consumer_home'))
        
    elif role == 'store':
        return redirect(url_for('store.store_home'))
    elif role == 'admin':
        return redirect(url_for('admin.admin_home'))
    else:
        return 'Unknown state', 400
# 檢查 token 是否過期的裝飾器
def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token_expiry_str = session.get('token_expiry')
            if not token_expiry_str:
                flash('Your session has expired. Please log in again.')
                return redirect(url_for('line_auth.login_line', role=role))
            
            token_expiry = datetime.fromisoformat(token_expiry_str).replace(tzinfo=pytz.UTC)
            utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
            
            if utc_now > token_expiry:
                flash('Your session has expired. Please log in again.')
                return redirect(url_for('line_auth.login_line', role=role))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator