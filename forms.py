from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
import pymongo
from pymongo import MongoClient
from wtforms import validators, ValidationError


cluster = MongoClient("mongodb+srv://SNSTeam:1234@mycluster.wrkyk.mongodb.net/IAS_Project?retryWrites=true&w=majority")

db = cluster["IAS_Project"]
deploy_info = db["deployment_info"]

class ContactForm(FlaskForm):
    #lst=[('java', 'Java'),('py', 'Python')]
    
    #lst=["a1","a2","a3"]
    lst=[]
    x=deploy_info.find()
    for data in x:
        #print(data)
        #print(type (data))
        #print(data['_id'])
        lst.append(data["_id"])
    application_option = SelectField('Choose The Application', choices = lst)
    #submit = SubmitField("Send")