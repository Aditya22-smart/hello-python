from flask import Flask, request, jsonify
import joblib, numpy as np
from datetime import datetime

app = Flask(__name__)
model = joblib.load("iris_model.pkl")
LOG_FILE = "/var/log/ml_api.log"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)[0]
    log = {
        'timestamp': datetime.utcnow().isoformat(),
        'input': data['features'],
        'prediction': str(prediction)
    }
    with open(LOG_FILE, 'a') as f:
        f.write(str(log) + "\n")
    return jsonify({'prediction': str(prediction)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
