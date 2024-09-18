from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    lot_size = None
    if request.method == 'POST':
        try:
            # Retrieve the form data
            capital = float(request.form['capital'])
            risk_percentage = float(request.form['risk_percentage'])
            stop_loss_points = float(request.form['stop_loss_points'])

            # Calculate the lot size
            risk_amount = capital * (risk_percentage / 100)
            lot_size = risk_amount / stop_loss_points
        except (ValueError, ZeroDivisionError):
            lot_size = "Invalid input. Please check your values."

    return render_template('calculator.html', lot_size=lot_size)

if __name__ == '__main__':
    app.run(debug=True)
