from flask import Flask, render_template, request

app = Flask(__name__)

POINT_VALUE = 10   # $10 per point
TP_POINTS = 100    # Take-profit distance in points


@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    total_loss = 0.0
    total_max_loss = 0.0
    capital = ""
    hedges = ""
    zone = ""
    risk_percent = ""
    error = None

    if request.method == 'POST':
        capital = request.form.get('capital', '').strip()
        hedges = request.form.get('hedges', '').strip()
        zone = request.form.get('zone', '').strip()
        risk_percent = request.form.get('risk_percent', '').strip()

        try:
            capital = float(capital.replace(',', '.'))
            hedges = int(hedges)
            zone = float(zone.replace(',', '.'))
            risk_percent = float(risk_percent.replace(',', '.'))

            if capital <= 0:
                raise ValueError("Capital must be greater than zero.")
            if hedges < 1:
                raise ValueError("Number of hedges must be at least 1.")
            if zone <= 0:
                raise ValueError("Zone size must be greater than zero.")
            if not (0 < risk_percent <= 100):
                raise ValueError("Risk percent must be between 0 and 100.")

            total_max_loss = capital * (risk_percent / 100)
            losses = []

            for i in range(hedges):
                if i == 0:
                    lot = round(total_max_loss / (zone * POINT_VALUE * (2 ** (hedges - 1))), 2)
                else:
                    required_recovery = sum(losses)
                    lot = round(required_recovery / (TP_POINTS * POINT_VALUE), 2)

                loss = round(lot * zone * POINT_VALUE, 1)
                loss_pct = round((loss / capital) * 100, 2)
                profit_if_tp = round(lot * TP_POINTS * POINT_VALUE, 1)
                total_loss += loss

                losses.append(loss)
                results.append({
                    'hedge_num': i + 1,
                    'lot_size': lot,
                    'loss_dollars': loss,
                    'loss_percent': loss_pct,
                    'profit': profit_if_tp,
                    'recovery': round(sum(losses[:-1]), 1),
                })

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = "An unexpected error occurred. Please check your inputs."
            app.logger.error("Unexpected error in index: %s", e)

    return render_template('index.html',
                           results=results,
                           total_loss=round(total_loss, 1),
                           total_max_loss=round(total_max_loss, 1),
                           capital=capital,
                           hedges=hedges,
                           zone=zone,
                           risk_percent=risk_percent,
                           error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
