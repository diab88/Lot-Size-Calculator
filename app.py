from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    total_loss = 0
    total_max_loss = 0
    capital = ""
    hedges = ""
    zone = ""
    risk_percent = ""

    if request.method == 'POST':
        try:
            capital = float(str(request.form['capital']).replace(',', '.'))
            hedges = int(request.form['hedges'])
            zone = float(str(request.form['zone']).replace(',', '.'))
            risk_percent = float(str(request.form['risk_percent']).replace(',', '.'))

            # Constants
            point_value = 10  # $10 per point
            tp_points = 100
            total_max_loss = capital * (risk_percent / 100)

            losses = []
            lot_sizes = []

            for i in range(hedges):
                if i == 0:
                    # First hedge can use some portion of the loss budget
                    lot = round(total_max_loss / (zone * point_value * (2 ** (hedges - 1))), 2)
                else:
                    required_recovery = sum(losses)
                    lot = round(required_recovery / (tp_points * point_value), 2)
                loss = round(lot * zone * point_value, 1)
                loss_pct = round((loss / capital) * 100, 2)
                profit_if_tp = round(lot * tp_points * point_value, 1)

                lot_sizes.append(lot)
                losses.append(loss)
                total_loss += loss

                results.append({
                    'hedge_num': i + 1,
                    'lot_size': lot,
                    'loss_dollars': loss,
                    'loss_percent': loss_pct,
                    'profit': profit_if_tp if i == 0 else sum(losses[:-1])  # Compensate prior
                })

        except Exception as e:
            print("Error:", e)

    return render_template('index.html',
                           results=results,
                           total_loss=round(total_loss, 1),
                           total_max_loss=round(total_max_loss, 1),
                           capital=capital,
                           hedges=hedges,
                           zone=zone,
                           risk_percent=risk_percent)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
