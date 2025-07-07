from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    capital = num_hedges = zone_size = risk_percent = None
    total_loss = total_max_loss = 0

    if request.method == "POST":
        try:
            capital = float(str(request.form["capital"]).replace(",", "."))
            num_hedges = int(request.form["hedges"])
            zone_size = float(str(request.form["zone"]).replace(",", "."))
            risk_percent = float(str(request.form["risk_percent"]).replace(",", "."))

            point_value = 5  # $5 per 1.0 lot per point
            tp_points = 100

            total_max_loss = (risk_percent / 100) * capital
            losses = []
            lot_sizes = []
            profits = []

            # Calculate hedge lot sizes backward to fulfill compensation requirement
            remaining_loss_to_compensate = 0

            for i in reversed(range(1, num_hedges + 1)):
                if i == 1:
                    # First hedge: can make profit after compensating all others
                    profit_target = total_max_loss
                else:
                    # Other hedges only compensate previous losses
                    profit_target = remaining_loss_to_compensate

                lot_size = profit_target / (tp_points * point_value)
                lot_size = round(lot_size, 2)

                loss = lot_size * zone_size * point_value
                loss_percent = (loss / capital) * 100
                tp_profit = lot_size * tp_points * point_value

                lot_sizes.insert(0, lot_size)
                losses.insert(0, (loss, loss_percent))
                profits.insert(0, tp_profit)

                remaining_loss_to_compensate += loss

            results = [
                {
                    "hedge_num": i + 1,
                    "lot_size": lot_sizes[i],
                    "loss_dollars": round(losses[i][0], 2),
                    "loss_percent": round(losses[i][1], 2),
                    "profit": round(profits[i], 2)
                }
                for i in range(num_hedges)
            ]

            total_loss = round(sum([r["loss_dollars"] for r in results]), 2)
            total_max_loss = round(total_max_loss, 2)

        except Exception as e:
            print("Error:", e)

    return render_template("index.html", results=results, capital=capital, hedges=num_hedges,
                           zone=zone_size, risk_percent=risk_percent,
                           total_loss=total_loss, total_max_loss=total_max_loss)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
