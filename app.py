from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
import io
import os
import pickle


#loading trained MLP model. The following function is used to get symptoms as input and predict the result
mlp = pickle.load(open('finalized_model.sav', 'rb'))



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
      #name = request.form['name']
      email = request.form.get('email')
      password = request.form.get('password')
      if email:
         return render_template('index.html')
      
      '''
      # Retrieve the password for the entered email from Azure Blob Storage
      blob_name = f"{email}.txt"
      blob_client = container_client.get_blob_client(blob_name)
      blob_data = blob_client.download_blob().content_as_text()
      if blob_data == password:
         return render_template('hello.html', name=name)
      else:
         # Passwords don't match, redirect to index page
         print('Incorrect email or password -- redirecting')
         return redirect(url_for('index'))
       '''
   
   # Render the index page with the login form
   return render_template('sign-in.html')


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        # Get the uploaded file
        text = request.form['text']
        if text:
            return render_template('index.html', detectedValue='random')
    # Render the hello page with the image upload form
    return render_template('index.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
   if request.method == 'POST':
      # Get the user's information from the form
      name = request.form.get('name')
      email = request.form.get('email')
      password = request.form.get('password')
      # Redirect to the index page
      return redirect(url_for('index'))

   # If the request method is GET, render the signup page
   return render_template('sign-up.html')



if __name__ == '__main__':
   app.run()
