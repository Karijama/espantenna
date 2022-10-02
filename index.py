from flask import Flask, render_template, url_for, request
import pyrebase
from flask_bootstrap import Bootstrap
import urllib.request, json


app = Flask(__name__)
bootstrap = Bootstrap(app)

config = {
    'apiKey': "AIzaSyCUXMY86neXeFTFeAbHnjxlEQsYq4OQh28",
    'databaseURL': "https://espada-e9ff8-default-rtdb.firebaseio.com",
    'authDomain': "espada-e9ff8.firebaseapp.com",
    'projectId': "espada-e9ff8",
    'storageBucket': "espada-e9ff8.appspot.com",
    'messagingSenderId': "147002329373",
    'appId': "1:147002329373:web:b4921015e369826c16b9f4",
    'measurementId': "G-V9C4FDY0G2"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
with urllib.request.urlopen("https://gsn.yktaero.space/api/stations/?format=json") as url:
    data = json.load(url)

@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/index', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        email=request.form['email']
        pas = request.form['pas']
        try:
            auth.sign_in_with_email_and_password(email,pas)
            user_info = auth.sign_in_with_email_and_password(email,pas)
            account_info = auth.get_account_info(user_info['idToken'])
            if account_info['user'][0]['emailVeri'] == False:
                verify_message = 'Please, verify your email'
                return render_template('base.html',umessage = verify_message)
            return render_template('index.html')
        except:
            unsuccess = 'Please check your credentials'
            return render_template('index.html', umessage = unsuccess)
    return render_template('base.html')
@app.route('/registration',methods=['POST','GET'])
def regist():
    if request.method == 'POST':
        pas0 = request.form['pas0']
        pas1 = request.form['pas1']
        if pas0 == pas1:
            try:
                email = request.form['email']
                pasw = request.form['pas1']
                new_user=auth.create_user_with_email_and_password(email,pasw)
                auth.send_email_verification(new_user['idToken'])
                return render_template('verify.html')
            except:
                existing = 'Check passwords'
                return render_template('registration.html',exist_message=existing)
    return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)
