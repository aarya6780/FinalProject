# -*- coding: utf-8 -*-
from datetime import datetime,timedelta
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
import io
import os
import pickle




app = Flask(__name__)



from flask_sqlalchemy import SQLAlchemy

app.secret_key='test123'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['TESTING']=True
app.config['SQLALCHEMY_TRACK_MODIFICATION']=True
app.config['SQLALCHEMY_ECHO']= False
app.config['SQLALCHEMY_MAX_OVERFLOW']=0



app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:test123@localhost:5432/test1'
db=SQLAlchemy(app)


app.app_context().push()
from controller import routes



   