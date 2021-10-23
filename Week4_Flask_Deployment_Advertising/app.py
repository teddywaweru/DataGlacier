"""
Flask App to run the Advertising Prediction Model
"""
import pickle
from pathlib import Path
from flask import Flask, request, render_template


app = Flask(__name__)
#Enable reloading changes on HTML pages.
app.config['TEMPLATES_AUTO_RELOAD'] = True

    #Load the Prediction Model to prediction_model
def load_model():
    """
    create functions for loading the models
    """
    script_location = Path(__file__)
    prediction_model = pickle.load(open(script_location / '../adv_pred_model.pkl', 'rb'))
    return prediction_model

#create functions for carrying out predictions
def prediction(age, internet_time, site_time, area_income):
    """
    Carry out prediction depending on variables provided.
    """
    prediction_value = load_model().predict([age, internet_time, site_time, area_income])

    return prediction_value

#create routes to be accessed by the HTML page. Index Page
@app.route('/')
def index():
    """
    Index function to render index page
    """
    return render_template('index.html')


#create routes to be accessed by the HTML page. Predict Render
@app.route('/predict')
def predict():
    """
    Collect form data, store & pass to prediction function.
    """
    age = request.form.get('age')
    internet_time = request.form.get('internet_time')
    site_time = request.form.get('site_time')
    area_income = request.form.get('area_income')

    prediction(age, internet_time, site_time, area_income)

    predicted = True

    render_template('index.html',
                    predicted = predicted, age = age, internet_time = internet_time,
                    site_time = site_time, area_income = area_income )

#initialize application
if __name__ == '__main__':
    app.run() #run application
    load_model() #load model early
