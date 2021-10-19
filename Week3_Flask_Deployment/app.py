"""Landing page for Flask Deployment app"""


import pickle
from flask import Flask
from flask import render_template
# from flask.wrappers import Request

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
# prediction_model = None


class LoadModel(object):
    """Loading model Function"""
    def __init__(self):
        self.prediction_model = None

    def load_model(self):
        '''Loading Model'''
        self.prediction_model = pickle.load(open('model.pkl','rb'))
        return self.prediction_model

@app.route('/')
def index():
    """Landing Page loading"""
    return render_template('index.html')

@app.route('/get_prediction', methods = ['POST'])
def get_prediction():
    """Landing Page loading"""
    return render_template('secondpage.html')


if __name__ == '__main__':
    app.run()
