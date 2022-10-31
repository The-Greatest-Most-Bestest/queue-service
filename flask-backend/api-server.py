import string
from flask import Flask
from pymongo import MongoClient

import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# PyMongo Stuff
client = MongoClient("mongodb+srv://langgeng:vv8q1OJCO3ANbe9b@clusterfuck.9jonez9.mongodb.net/?retryWrites=true&w=majority")
db = client.queueDB



# API Route
@app.route("/")
def home():
    return "Welcome to the Queue Service App"

@app.route("/team")
def team():
    return {"members": ["Matthew", "Brianna", "Lily", "Riley", "Leo"]}

@app.route("/queue")
def queue():
    return db.list_collection_names()

@app.route("/push/<collection>/<fname>/<lname>/<broncoID>")
def test(collection, fname, lname, broncoID):
    coll = db[collection]
    seqID = coll.countDocuments({})
    print(seqID)
    coll.insert_one(
        {
            'seqID' : seqID,
            'fname' : fname,
            'lname' : lname,
            'broncoID' : broncoID,
            'time' : datetime.datetime.now()
        }
    )
    return "pushedUser"

@app.route("/email")
def email():
    receiver = '130nardolanggeng@gmail.com'
    location = 'BSC Games Room'
    queue_name = 'PS4 Console'
    sendEmail(receiver, location, queue_name)
    return('email sent')

def sendEmail(send_to, location, queue_name):
    subject = 'It is your turn for ' + queue_name + ' at ' + location
    mail_content = 'Mail content yada yada yada. \n Ⓒ GMB 2022.'

    sender_address = 'gmbcs4800@gmail.com'
    sender_pass = 'rbrqwjrgxonlzsli'
    receiver_address = send_to

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

    return 'email sent check'


if __name__ == "__main__":
    app.run()




