# app.py
from flask import Flask, render_template, request
import os

app = Flask(__name__)

POINT_VALUE = 5  # $5 per 1.0 lot
TAKE_PROFIT_POINTS = 100
MAX_RISK_PERCENT = 0.09


def calculate_hedge_lots(capital, hedge_count, zone):
    max_total_loss = capital * MAX_RISK_PERCENT

    # We assume geometric progression: lot_i = base_lot * multiplier^i
    # Goal: Find base_lot such that:
    # sum(loss_i) <= max_total_loss AND last TP >= sum(losses before last)

    # Try common multipliers: 1.5x, 2x, 2.5x
    best_result = []
    best_total_loss = None
    for multiplier in [1.5, 2, 2.2]:
        base_lot = 0.01
        while base_lot < 100:
            lots = [round(base_lot * (multiplier ** i), 2) for i in range(hedge_count)]
            losses = [lot * zone * POINT_VALUE for lot in lots]
            total_loss = sum(losses)
            
            if total_loss > max_total_loss:
                break  # stop testing this base_lot

            last_profit = lots[-1] * TAKE_PROFIT_POINTS * POINT_VALUE
            if last_profit >= sum(losses[:-1]):
                best_result = lots
                best_total_loss = total_loss
                break

            base_lot += 0.01

        if best_result:
            break  # stop trying other multipliers

    # Format results
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
