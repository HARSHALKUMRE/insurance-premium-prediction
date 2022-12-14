import pandas as pd
from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib

# Create Flask object to Run
app = Flask(__name__)

# Load the model from the File

model_load = joblib.load('./model/premium_prediction_model.pkl')


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/predict", methods=['POST'])
def predict():
    # For rendering results on HTML GUI
    if request.method == 'POST':
        age = request.form['age']
        bmi = request.form['bmi']
        region_northwest = request.form['region_northwest']
        region_southeast = request.form['region_southeast']
        region_southwest = request.form['region_southwest']
        sex = request.form['sex']
        smoker = request.form['smoker']
        children = request.form['children']
        input_val = [age,
                     bmi,
                     region_northwest,
                     region_southeast,
                     region_southwest,
                     sex,
                     smoker,
                     children]
        final_features = [np.array(input_val)]
        df = pd.DataFrame(final_features)

        output = model_load.predict(df)
        result = "%.2f" % round(output[0], 2)


        return render_template('home.html', prediction_text=f'Insurance Premium is $ {result} ')
    else:
        return render_template('home.html')


# App Code for Testing on Postman
@app.route("/predict_api", methods=['POST', 'GET'])
def predict_api():
    print(" request.method :", request.method)
    if request.method == 'POST':
        age = request.json['age']
        bmi = request.json['bmi']
        region_northwest = request.json['region_northwest']
        region_southeast = request.json['region_southeast']
        region_southwest = request.json['region_southwest']
        sex = request.json['sex']
        smoker = request.json['smoker']
        children = request.json['children']
        input_val = [age,
                     bmi,
                     region_northwest,
                     region_southeast,
                     region_southwest,
                     sex,
                     smoker,
                     children]
        final_features = [np.array(input_val)]

        output = model_load.predict(final_features).tolist()
        return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True, port=5000)