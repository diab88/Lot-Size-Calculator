# app.py
from flask import Flask, render_template, request
import os

app = Flask(__name__)

POINT_VALUE = 5  # $5 per 1.0 lot
TAKE_PROFIT_POINTS = 100
MAX_RISK_PERCENT = 0.09


def calculate_hedge_lots(capital, hedge_count, zone):
    max_total_loss = capital * MAX_RISK_PERCENT

    lots = []
    total_loss = 0

    base_lot = 0.01
    increment = 0.01

    while True:
        temp_lots = [round(base_lot + i * increment, 2) for i in range(hedge_count)]
        temp_losses = [lot * zone * POINT_VALUE for lot in temp_lots]
        temp_total_loss = sum(temp_losses)
        temp_last_profit = temp_lots[-1] * POINT_VALUE * TAKE_PROFIT_POINTS

        if temp_total_loss <= max_total_loss and temp_last_profit >= sum(temp_losses[:-1]):
            lots = temp_lots
            total_loss = temp_total_loss
            break

        increment += 0.01
        if increment > 5:
            break

    results = []
    for i, lot in enumerate(lots):
        dollar_loss = lot * zone * POINT_VALUE
        percent_loss = (dollar_loss / capital) * 100
        results.append({
            'hedge': i + 1,
            'lot_size': lot,
            'loss_dollars': round(dollar_loss, 2),
            'loss_percent': round(percent_loss, 2),
            'profit_if_tp': round(lot * POINT_VALUE * TAKE_PROFIT_POINTS, 2)
        })

    return results, round(total_loss, 2), max_total_loss


@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    total_loss = 0
    max_loss = 0
    capital = ''
    hedge_count = ''
    zone = ''
    if request.method == 'POST':
        capital = float(request.form['capital'])
        hedge_count = int(request.form['hedge_count'])
        zone = int(request.form['zone'])

        results, total_loss, max_loss = calculate_hedge_lots(capital, hedge_count, zone)

    return render_template('index.html', results=results, total_loss=total_loss,
                           max_loss=max_loss, capital=capital, hedge_count=hedge_count, zone=zone)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
