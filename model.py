import pickle
import numpy as np

# Load the model at module level so it's loaded only once
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict_stock_close(open_val, high, low, volume, day, month, weekday):
    features = np.array([[open_val, high, low, volume, day, month, weekday]])
    prediction = model.predict(features)
    return prediction[0] 