from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import db, Music
from ..logs import new_log
from flask_login import login_required, current_user
from ..config import CRYPTO_BOT_TOKEN
from ..models import Order
import requests

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/buy/<int:song_id>')
def buy(song_id):
    song = Music.query.get_or_404(song_id)
    new_log(f"Пользователь зашел на страницу покупки трека {song.title}")
    return render_template('shop.html', song=song)


@shop_bp.route('/create_payment/<int:song_id>/<license_type>')
@login_required
def create_payment(song_id, license_type):
    song = Music.query.get_or_404(song_id)
    new_log(f"Пользователь зашел на страницу оплаты трека {song.title}, хочет заплатить за {license_type} ")    
    # Определяем цену в зависимости от лицензии
    prices = {
        'mp3': song.price_mp3,
        'wav': song.price_wav,
        'trackout': song.price_track_out,
        'exclusive': song.price_exclusive
    }
    amount = prices.get(license_type)

    # Запрос к Crypto Bot API
    headers = {"Crypto-Pay-API-Token": CRYPTO_BOT_TOKEN}
    payload = {
        "asset": "USDT", # Можно сделать выбор валюты
        "amount": str(amount),
        "description": f"Покупка {song.title} ({license_type})",
        "payload": f"order_{current_user.id}_{song.id}", # Хинт для нас
        "paid_btn_name": "callback",
        "paid_btn_url": url_for('index', _external=True)
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    data = response.json()

    if data['ok']:
        # Сохраняем заказ в БД
        new_order = Order(
            user_id=current_user.id,
            music_id=song.id,
            amount=amount,
            currency="USDT",
            invoice_id=data['result']['invoice_id']
        )
        db.session.add(new_order)
        db.session.commit()
        
        # Перенаправляем пользователя на оплату
        return redirect(data['result']['pay_url'])
    else:
        flash("Ошибка при создании счета")
        return redirect(url_for('buy', song_id=song_id))
