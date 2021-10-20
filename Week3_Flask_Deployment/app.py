"""Landing page for Flask Deployment app"""


import sys
import pickle
from flask import Flask, request
from flask import render_template




app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
# prediction_model = None


class LoadModel(object):
    """Loading model Function"""
    def __init__(self):
        self.prediction_model = None

    def load_model(self):
        '''Loading Model'''
        with open('model.pkl','rb') as f:
            self.prediction_model = pickle.load(f)
        print('Successfully loaded model')
        return self.prediction_model

    def prediction(self, trial):
        x = self.prediction_model(trial)
        return (x)

@app.route('/')
def index():
    """Landing Page loading"""
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def get_prediction():
    """Landing Page loading"""
    age = request.form.get('age')
    sibling = request.form.get('sibling')
    parents = request.form.get('parents')

    x = LoadModel().prediction([1,77,8])


    # sys.stdout.write(age)
    # logger.info()
    predict = True
    return render_template('index.html', predict = predict, age = age, x = x )


if __name__ == '__main__':
    LoadModel().load_model()
    app.run()
