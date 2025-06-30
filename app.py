# app.py
from flask import Flask, render_template, request
import os

app = Flask(__name__)

POINT_VALUE = 5  # $5 per 1.0 lot
TAKE_PROFIT_POINTS = 100
MAX_RISK_PERCENT = 0.09


def calculate_hedge_lots(capital, hedge_count, zone):
    max_total_loss = capital * MAX_RISK_PERCENT

    # Strategy:
    # - First hedge can make profit (freely chosen)
    # - Each following hedge must only recover previous loss, no extra profit

    # Start by guessing first hedge lot size
    base_lot = 0.01
    best_result = []
    best_total_loss = 0

    while base_lot < 100:
        lots = [base_lot]
        losses = [base_lot * zone * POINT_VALUE]

        for i in range(1, hedge_count):
            accumulated_loss = sum(losses)
            lot = accumulated_loss / (TAKE_PROFIT_POINTS * POINT_VALUE)
            losses.append(lot * zone * POINT_VALUE)
            lots.append(lot)

        total_loss = sum(losses)
        if total_loss > max_total_loss:
            break  # Exceeded allowed risk

        best_result = lots
        best_total_loss = total_loss
        base_lot += 0.01

    if not best_result:
        return [], 0, max_total_loss

    results = []
    accumulated_loss = 0
    for i, lot in enumerate(best_result):
        dollar_loss = lot * zone * POINT_VALUE
        percent_loss = (dollar_loss / capital) * 100

        if i == 0:
            tp_profit = lot * TAKE_PROFIT_POINTS * POINT_VALUE
        else:
            tp_profit = accumulated_loss  # strictly compensating prior loss only

        accumulated_loss += dollar_loss

        results.append({
            'hedge': i + 1,
            'lot_size': round(lot, 2),
            'loss_dollars': round(dollar_loss, 2),
            'loss_percent': round(percent_loss, 2),
            'profit_if_tp': round(tp_profit, 2)
        })

    return results, round(best_total_loss, 2), round(max_total_loss, 2)


@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    total_loss = 0
    max_loss = 0
    capital = ''
    hedge_count = ''
    zone = ''
    if request.method == 'POST':
        capital = float(request.form['capital'].replace(',', '.'))
        hedge_count = int(request.form['hedge_count'])
        zone = int(request.form['zone'])

        results, total_loss, max_loss = calculate_hedge_lots(capital, hedge_count, zone)

    return render_template('index.html', results=results, total_loss=total_loss,
                           max_loss=max_loss, capital=capital, hedge_count=hedge_count, zone=zone)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
