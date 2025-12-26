from app import create_app
from flask import session, redirect, url_for, request, Blueprint

app = create_app()

# 1 доллар = 90 рублей
EXCHANGE_RATE = 90

@app.template_filter('format_price')
def format_price(value):
    if value is None:
        return ""
    
    currency = session.get('currency', 'rub') # По умолчанию рубли
    
    if currency == 'usd':
        # БАЗА В ДОЛЛАРАХ -> ОСТАВЛЯЕМ КАК ЕСТЬ
        return f"${value:.2f}"
    else:
        # БАЗА В ДОЛЛАРАХ -> КОНВЕРТИРУЕМ В РУБЛИ (Умножаем)
        converted = float(value) * EXCHANGE_RATE
        return f"{converted} ₽"
if __name__ == '__main__':
    app.run(debug=True)