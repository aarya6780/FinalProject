# importing the package  
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from app import app
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
import io
import os
import pickle
from app import db
import random 
import string
# importing the models for database
from model.login import loginTable
from model.user import Register
from model.survey import surveyTable
from model.detector import detectorTable

import language_tool_python  

  
# using the tool  
my_tool = language_tool_python.LanguageTool('en-US')  
   
def corrector(my_text):   
 
    my_matches = my_tool.check(my_text)    
    myMistakes = []  
    myCorrections = []  
    startPositions = []  
    endPositions = []  
  
# using the for-loop  
    for rules in my_matches:  
        if len(rules.replacements) > 0:  
            startPositions.append(rules.offset)  
            endPositions.append(rules.errorLength + rules.offset)  
            myMistakes.append(my_text[rules.offset : rules.errorLength + rules.offset])  
            myCorrections.append(rules.replacements[0])  
  
    my_NewText = list(my_text)   
  
    # rewriting the correct passage  
    for n in range(len(startPositions)):  
        for i in range(len(my_text)):  
            my_NewText[startPositions[n]] = myCorrections[n]  
            if (i > startPositions[n] and i < endPositions[n]):  
                my_NewText[i] = ""  
    return "".join(my_NewText) 



#loading trained MLP model.
mlp = pickle.load(open('/opt/FinalProject/fp_1/finalized_model.sav', 'rb'))
# vectorizer = pickle.load(open('/Users/aaryadoshi/Documents/fp_1/vectorizer.pickle','rb'))
vectorizer = pickle.load(   open('/opt/FinalProject/fp_1/vectorizer.pickle','rb'))
session = []

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    if request.method == 'POST':
        #name = request.form['name']
        uname = request.form['uname']
        password = request.form['psw']
        login_obj = loginTable()
        login_obj.logged_useremail = uname
        login_obj.logged_password = password
        x = loginTable.query.filter_by(logged_useremail = login_obj.logged_useremail, logged_password = login_obj.logged_password )
        userLists= [ i.as_dict() for i in x]
        
        print(userLists)
        if userLists:
            response = make_response(redirect(url_for('home')))
            response.set_cookie('logged_secret',value=userLists[0].get('logged_secret'))
            session.append(userLists[0].get('logged_secret'))
            return response
        else:
            
            return redirect('/')
        

# Survey Form
@app.route('/case',methods=['GET','POST'])
def testCase():
    if request.cookies.get('logged_secret') not in session:
        return redirect('/')    
    if request.method == 'POST':

        fname = request.form.get('First')
        lname = request.form.get('Last')
        ratings = request.form.get('ratings')
        radio_yes = request.form.get('radio_yes')
        radio_no = request.form.get('radio_no')
        feedbacks = request.form.get('feedbacks')
        is_recommendable = "no"

        userDetail = loginTable.query.filter_by(logged_secret = request.cookies.get('logged_secret'))
        dictDetail = [i.as_dict() for i in userDetail]
        userEmail = dictDetail[0].get("logged_useremail")

        if radio_yes == "1":
            is_recommendable = "yes"

        SurveyData_obj = surveyTable()
        SurveyData_obj.firstname = fname
        SurveyData_obj.lastname = lname
        SurveyData_obj.ratings = ratings
        SurveyData_obj.is_recommendable = is_recommendable
        SurveyData_obj.feedbacks = feedbacks
        SurveyData_obj.email = userEmail
        db.session.add(SurveyData_obj)
        db.session.commit()
        

      # Get the user's information from the form
        val = loginTable.query.filter_by(logged_secret = request.cookies.get('logged_secret'))
        test = [i.as_dict() for i in val]

        if test[0].get("logged_useremail") :
            send_mail(test[0].get("logged_useremail"))
    return redirect(url_for('index_home'))

#function to send mail
def send_mail(username):
    sender = "doshiaarya007@gmail.com"
    password = "gbfctpxwdwhhfqfc"
    receiver = username
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Survey Completed"
    body = "Dear Sir/Ma'am,\n We have received your reviews on our app.\n We will closely look into it and do the neccessary changes to make your experience even better.\n Best Regards, \n Team 14"
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()

#AI detector route
@app.route('/index_home', methods=['GET', 'POST'])
def index_home():
    if request.cookies.get('logged_secret') not in session:
        return redirect('/')  
    if request.method == 'POST':      #name = request.form['name']
      text = request.form['text']    
      X_test = vectorizer.transform([text]) 
      y_pred = mlp.predict(X_test)     
      text = request.form['text']
      if text:         
          return render_template('index.html', result='random')
         # Render the index page with the login form
    return render_template('index.html')
    

#Home page    
@app.route('/home',methods=['GET'])
def home_page():
    if request.cookies.get('logged_secret') not in session:
        return redirect('/')
    return render_template('home.html')

#UI of Survey Form
@app.route('/form',methods=['GET'])
def form_page():
    if request.cookies.get('logged_secret') not in session:
        return redirect('/')
    return render_template('form.html')

#AI Detector Submit 
@app.route('/submit_form', methods=['POST'])
def submit_form():
    # process the form data here
    if request.cookies.get('logged_secret') not in session:
        return redirect('/')  
    text = request.form['text']
    if not text:
        return redirect('/index_home')
    X_test = vectorizer.fit_transform([text]) 
    answer = mlp.predict(X_test)
    prediction = answer[0]
    prob = mlp.predict_proba(X_test)[0][1]*100
    
    userDetail = loginTable.query.filter_by(logged_secret = request.cookies.get('logged_secret'))
    dictDetail = [i.as_dict() for i in userDetail]
    userEmail = dictDetail[0].get("logged_useremail")

    if prediction == 1.0:
        result = "The text might be written by AI as the probability for the given text to be written by AI is " + str('{:.2f}'.format(prob)) + "%"
        detector_obj = detectorTable()
        detector_obj.input = text
        detector_obj.value = str('{:.2f}'.format(prob)) 
        detector_obj.user_email = userEmail
        db.session.add(detector_obj)
        db.session.commit()
        return render_template('index.html', test=result)
    if prediction == 0.0:
        result = "The text might not be written by AI as the probability for the given text to be written by AI is " + str('{:.2f}'.format(prob)) + "%"
        detector_obj = detectorTable()
        detector_obj.input = text
        detector_obj.value = str('{:.2f}'.format(prob)) 
        detector_obj.user_email = userEmail
        db.session.add(detector_obj)
        db.session.commit()
        return render_template('index.html', test=result)
    

#Logout Route    
@app.route('/logoff',methods=['get'])
def logOff():
    logged_secret = request.cookies.get('logged_secret')
    response = make_response(redirect('/'))
    response.set_cookie('logged_secret', "", max_age=0)
    session.clear()
    return response

#Regsiter User
@app.route('/registeruser',methods=['GET','POST'])
def register():
    if request.method == 'POST':
      # Get the user's information from the form
      fname = request.form.get('fname')
      lname = request.form.get('lname')
      email = request.form.get('mail')
      contact = request.form.get('contact')
      password = request.form.get('psw')

      login_data = loginTable()
      login_data.logged_useremail = email
      login_data.logged_password = password
      login_data.logged_secret = "".join((random.choice(string.ascii_letters+string.digits)) for x in range(10))
      db.session.add(login_data)
      db.session.commit()

      user_data = Register()
      user_data.first_name = fname
      user_data.last_name = lname
      user_data.email_id = email
      user_data.contact = contact
      user_data.user_logged_id = login_data.logged_id
      db.session.add(user_data)
      db.session.commit()

      # Redirect to the index page
      return redirect(url_for('login'))
    else:
      return render_template('sign-up.html')

    
from textblob import TextBlob

#Spell Check 
@app.route('/spellcheck', methods=['POST', 'GET'])
def spellcheck():
    if request.cookies.get('logged_secret') not in session:
        return redirect('/')  
    if request.method == 'POST':
        text = request.form['text']
        #sentence = TextBlob(text)
        #result = sentence.correct()
        result = corrector(text)
        return render_template('spellcheck.html', test=result)
    return render_template('spellcheck.html')


@app.route('/home', methods=['POST', 'GET']) 
def home():
    return render_template('home.html')

app = Flask(__name__, static_url_path='/static')

 
