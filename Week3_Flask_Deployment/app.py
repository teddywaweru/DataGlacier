from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/second_page')
def second_page():
    return render_template('secondpage.html')
   


if __name__ == '__main__':
    app.run()
