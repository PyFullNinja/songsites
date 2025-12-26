from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import db, Music
from ..telegram_bot import send
from ..logs import new_log


contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('/', methods=['GET', 'POST'])
def contacts():
    new_log("Пользователь зашел на страницу /contacts")
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        send(f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}")
        new_log(f"Пользователь отправил сообщение: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}")
        
        flash('Message sent successfully!')
        return redirect(url_for('contacts'))
    
    return render_template('contacts.html')

