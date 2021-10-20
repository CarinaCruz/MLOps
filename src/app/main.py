from flask import Flask, request
from flask_basicauth import BasicAuth
import pickle
import os

###### ML Model ######
columns = ["tamanho", "ano", "garagem"]
lr = pickle.load(open("../../models/lr.sav", "rb"))

###### Authentication ######
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

###### Routes ######
@app.route("/")
def home():
    return "App for House Prices Prediction"


@app.route("/predict_house_prices/", methods=['POST'])
@basic_auth.required
def predict_house_prices():
    data = request.get_json()
    input_data = [data[col] for col in columns]
    price = lr.predict([input_data])
    return str(price)
    
app.run(debug=True, host='0.0.0.0')