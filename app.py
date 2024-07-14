from flask import Flask, render_template, request, redirect
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import pandas as pd
from ntscraper import Nitter
import smtplib
import requests


# Initialize the Nitter scraper
scraper = Nitter(0)

from sklearn.decomposition import PCA

# import tweepy


rfc = joblib.load('twitter_models/rfc.joblib')
dtc = joblib.load('twitter_models/dtc.joblib')
knn = joblib.load('twitter_models/knn.joblib')
svc = joblib.load('twitter_models/svc.joblib')
log_reg = joblib.load('twitter_models/losreg.joblib')

models = [rfc, dtc, knn, svc, log_reg]

app = Flask(__name__)


# @app.route('/', methods =["GET", "POST"])
# def app_run():
#     username = request.form.get('username')
#     email_id = request.form.get('email_id')

#     if request.method == "POST":

#         profile_info = scraper.get_profile_info(username)

#         try:
#             user_input_features = extract_features(profile_info)
            
#         except:
#             send_email(email_id, False)
#             return redirect("https://twitter.com/i/flow/login", code=302)

#         send_email(email_id)
        
        
#         return render_template('main.html', account_existing = True, endpoint = '/')

#     else:
#         return render_template('main.html', endpoint = '/')


@app.route('/', methods =["GET", "POST"])
def view_details():
    
    if request.method == 'POST':

        username = request.form.get('username')
        email_id = request.form.get('email_id')

        # predictions_twitter, user_data = validate_twitter_account(request)

        profile_info = scraper.get_profile_info(username)

        try:
            user_input_features = extract_features(profile_info)
        except:
            send_email(email_id, False)
            return redirect("https://twitter.com/i/flow/login", code=302)
        
        send_email(email_id)
        train_path = 'train_final_twitter.csv'
        test_path = 'test_final_twitter.csv'

        train = pd.read_csv(train_path)
        test = pd.read_csv(test_path)

        x_train = train.iloc[:, :-1].values
        x_test = test.iloc[:, :-1].values

        sc = StandardScaler()
        x_train_sc = sc.fit_transform(x_train)
        x_test_sc = sc.transform(user_input_features)

        imputer = SimpleImputer(strategy='mean')
        x_train_imputed = imputer.fit_transform(x_train_sc)
        x_test_imputed = imputer.transform(x_test_sc)

        scaler = StandardScaler()
        x_train_imputed_scaled = scaler.fit_transform(x_train_imputed)
        x_test_imputed_scaled = scaler.transform(x_test_imputed)

        pca = PCA(n_components=2)
        x_train_sc_pca = pca.fit_transform(x_train_imputed_scaled)
        x_test_sc_pca = pca.transform(x_test_imputed_scaled)

        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(x_train_imputed)
        x_test_scaled = scaler.transform(x_test_imputed)


        fake_probabilities = []
        real_probabilities = []
        predictions = []

        user_input_scaled = x_test_imputed_scaled

        for model in models:
        
            if model == log_reg:
                user_input_scaled = x_test_sc_pca
                
            prediction = model.predict(user_input_scaled)
            prob = model.predict_proba(user_input_scaled)
            prob_percentage = prob[:, prediction] * 100
            prob_percentage = prob_percentage.item()
            

            if prediction[0] == 1: 
                prediction = "Fake"
                fake_probabilities.append(prob_percentage)
                real_probabilities.append(100 - prob_percentage)
            else: 
                prediction = "Real"
                real_probabilities.append(prob_percentage)
                fake_probabilities.append(100 - prob_percentage)
            
            predictions.append(prediction)

        user_data = []
        user_data.append(username)
        user_data.append(profile_info.get('name', ''))
        user_data.append(profile_info.get('stats', {}).get('followers', 0))
        user_data.append(profile_info.get('stats', {}).get('following', 0))
        user_data.append(profile_info.get('stats', {}).get('tweets', 0))
        user_data.append(profile_info.get('image'))
        user_data.append(profile_info.get('bio', ''))

        return render_template('main.html', account_existing = True, profile_info = profile_info, predictions=predictions, real_probabilities = real_probabilities, fake_probabilities = fake_probabilities, user_data=user_data, is_twitter = True, endpoint='/view_details')
    else:
        return render_template('main.html', end_point = '/view_details')
    
def count_words(text):
    words = text.split()
    return len(words)

def extract_features(profile_info):

    full_name = profile_info['name']
    screen_name = profile_info['username']
    followers_count = profile_info['stats']['followers']
    following_count = profile_info['stats']['following']
    posts_count = profile_info['stats']['tweets']
    profile_pic = int(bool(profile_info['image']))
    description_length = len(profile_info['bio'])
    num_words_in_full_name = count_words(full_name)
    is_equal_fullname_screenname = int(full_name.lower() == screen_name.lower())
    num_numbers_in_full_name = sum(c.isdigit() for c in full_name)
    num_numbers_in_screen_name = sum(c.isdigit() for c in screen_name)
    url=1
    return np.array([
        [num_numbers_in_full_name, num_words_in_full_name, num_numbers_in_screen_name,
         followers_count, following_count, posts_count, profile_pic, description_length, is_equal_fullname_screenname,url]
    ])


def send_email(email_id, is_created=True):
    public_ip = get_public_ip()
    location = get_location(public_ip)

    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()

    smtpserver.login("demoemail19122001@gmail.com", "reuwczxzmjfvabie")

    if is_created:
        message = f"Some one is trying to access a twitter account with your email id. \nIP ADDRESS: {public_ip}\nLOCATION: {location}"
    else:
        message = f"Some one is trying to create a twitter account with your email id. \nIP ADDRESS: {public_ip}\nLOCATION: {location}"

    smtpserver.sendmail("demoemail19122001@gmail.com", email_id, message)

    smtpserver.quit()


def get_public_ip():
    try:

        response = requests.get("https://httpbin.org/ip")

        if response.status_code == 200:
            data = response.json()
            public_ip = data.get("origin")
            return public_ip
        else:
            print(f"Error: Unable to fetch public IP address. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_location(ip_address):
    api_key = "2774678e1fd30a"

    api_url = f"http://ipinfo.io/{ip_address}/json"

    if api_key:
        api_url += f"?token={api_key}"

    response = requests.get(api_url)

    print(response.text)
    if response.status_code == 200:
        data = response.json()
        location = f'{data.get("city")}, {data.get("region")}, {data.get("country")}'
    else:
        print(f"Error: Unable to fetch location data. Status code: {response.status_code}")
    
    return location


if __name__ == '__main__':
    app.run(debug=True)