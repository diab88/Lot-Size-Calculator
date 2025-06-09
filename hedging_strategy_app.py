from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Hedging Strategy Calculator</title>
<h2>Hedging Strategy Calculator</h2>
<form method="post">
  Capital: <input type="number" step="any" name="capital" required><br><br>
  Zone Size (points): <input type="number" step="any" name="zone_size" required><br><br>
  Number of Hedges: <input type="number" name="hedges" required><br><br>
  Initial Risk (%): <input type="number" step="any" name="risk_pct" required><br><br>
  <div id="tp_inputs">
    Take Profit Points for each Hedge (comma separated):<br>
    <input type="text" name="tp_points" required><br><br>
  </div>
  <input type="submit" value="Calculate">
</form>

{% if table %}
  <h3>Results:</h3>
  <table border="1">
    <tr>
      <th>Hedge Round</th><th>Lot Size</th><th>Loss ($)</th><th>Loss (%)</th>
      <th>Cumulative Loss ($)</th><th>TP Target ($)</th><th>TP (%)</th>
    </tr>
    {% for row in table %}
    <tr>
      <td>{{ row['round'] }}</td><td>{{ row['lot_size'] }}</td><td>{{ row['loss'] }}</td>
      <td>{{ row['loss_pct'] }}</td><td>{{ row['cumulative_loss'] }}</td>
      <td>{{ row['tp'] }}</td><td>{{ row['tp_pct'] }}</td>
    </tr>
    {% endfor %}
  </table>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    table = []
    if request.method == 'POST':
        capital = float(request.form['capital'])
        zone_size = float(request.form['zone_size'])
        hedges = int(request.form['hedges'])
        risk_pct = float(request.form['risk_pct']) / 100
        tp_points = [float(x.strip()) for x in request.form['tp_points'].split(',')]

        cumulative_loss = 0

        for i in range(1, hedges + 1):
            tp_point = tp_points[i - 1] if i - 1 < len(tp_points) else tp_points[-1]
            if i == 1:
                loss = capital * risk_pct
                lot_size = loss / zone_size
            else:
                lot_size = cumulative_loss / tp_point
                loss = lot_size * zone_size
            cumulative_loss += loss
            tp = lot_size * tp_point
            table.append({
                'round': i,
                'lot_size': round(lot_size, 2),
                'loss': round(loss, 2),
                'loss_pct': round(loss / capital * 100, 2),
                'cumulative_loss': round(cumulative_loss, 2),
                'tp': round(tp, 2),
                'tp_pct': round(tp / capital * 100, 2),
            })

    return render_template_string(HTML_TEMPLATE, table=table)

if __name__ == '__main__':
    print("Starting Flask app on http://0.0.0.0:5050")
    app.run(host='0.0.0.0', port=5050)
