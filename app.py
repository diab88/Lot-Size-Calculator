# app.py
from flask import Flask, render_template, request
import os

app = Flask(__name__)

POINT_VALUE = 5  # $5 per 1.0 lot
TAKE_PROFIT_POINTS = 100
MAX_RISK_PERCENT = 0.09


def calculate_hedge_lots(capital, hedge_count, zone):
    max_total_loss = capital * MAX_RISK_PERCENT

    best_result = []
    best_total_loss = 0
    multipliers = [1.4, 1.5, 1.6, 1.7, 1.8, 2.0, 2.2, 2.5]

    for multiplier in multipliers:
        r = multiplier
        try:
            geometric_sum = (r**hedge_count - 1) / (r - 1)
            base_lot = max_total_loss / (zone * POINT_VALUE * geometric_sum)
        except (ZeroDivisionError, OverflowError):
            continue

        lots = [round(base_lot * (r**i), 2) for i in range(hedge_count)]
        losses = [lot * zone * POINT_VALUE for lot in lots]
        total_loss = sum(losses)
        last_tp = lots[-1] * TAKE_PROFIT_POINTS * POINT_VALUE

        if total_loss <= max_total_loss and last_tp >= sum(losses[:-1]):
            if total_loss > best_total_loss:
                best_result = lots
                best_total_loss = total_loss

    if not best_result:
        return [], 0, max_total_loss

    results = []
    for i, lot in enumerate(best_result):
        dollar_loss = lot * zone * POINT_VALUE
        percent_loss = (dollar_loss / capital) * 100
        tp_profit = lot * TAKE_PROFIT_POINTS * POINT_VALUE
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
