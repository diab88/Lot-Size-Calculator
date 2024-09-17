from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_lot_size(capital, risk_percent, stop_loss_pips, pip_value=10):
    risk_amount = capital * (risk_percent / 100)
    lot_size = risk_amount / (stop_loss_pips * pip_value)
    return lot_size

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            capital = float(request.form['capital'])
            risk_percent = float(request.form['risk_percent'])
            stop_loss_pips = float(request.form['stop_loss_pips'])

            lot_size = calculate_lot_size(capital, risk_percent, stop_loss_pips)
            return render_template('index.html', lot_size=lot_size, capital=capital, risk_percent=risk_percent, stop_loss_pips=stop_loss_pips)
        except ValueError:
            error = "Invalid input. Please enter numerical values."
            return render_template('index.html', error=error)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

