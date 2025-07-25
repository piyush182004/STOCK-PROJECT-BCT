from flask import Flask, render_template, request
from model import predict_stock_close
from ollama import get_professional_advice

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        open_val = float(request.form['open'])
        high = float(request.form['high'])
        low = float(request.form['low'])
        volume = float(request.form['volume'])
        day = int(request.form['day'])
        month = int(request.form['month'])
        weekday = int(request.form['weekday'])
        
        prediction = predict_stock_close(open_val, high, low, volume, day, month, weekday)
        prediction_rounded = round(prediction, 4)
        
        inputs = {
            'Open': open_val,
            'High': high,
            'Low': low,
            'Volume': volume,
            'Day': day,
            'Month': month,
            'Weekday': weekday
        }
        advice = get_professional_advice(inputs, prediction_rounded)
        
        return render_template('index.html', prediction=prediction_rounded, advice=advice)
    except Exception as e:
        return render_template('index.html', prediction=None, advice=f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True) 