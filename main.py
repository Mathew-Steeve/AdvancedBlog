from flask import Flask, render_template, request
import requests
import datetime as dt
import smtplib
import os
from dotenv import load_dotenv

app = Flask(__name__)

response = requests.get("https://api.npoint.io/8d8b31c3fa3510b2d111").json()

year = dt.datetime.now().year
mon = dt.datetime.today().strftime("%B")
day = dt.datetime.now().day


def send_mail(message):
    load_dotenv()
    sender_email = os.getenv('sender_email')
    password = os.getenv('password')
    receiver = os.getenv("receiver_mail")
    if not sender_email or not password or not receiver:
        raise ValueError("Missing sender, password, or receiver email in .env")

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(sender_email, password)
            s.sendmail(sender_email, receiver, message)
    except smtplib.SMTPAuthenticationError as e:
        print("AUTH ERROR:", e)
    except Exception as e:
        print("ERROR SENDING EMAIL:", e)


@app.route("/")
def home():
    return render_template("index.html", r=response, yr=year, m=mon, d=day)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.post("/contact")
def receive():
    message = (f"{request.form['username']}\n"
               f"{request.form['email']}\n"
               f"{request.form['phone']}\n"
               f"{request.form['message']}")
    print(request.form['username'])
    print(request.form['email'])
    print(request.form['phone'])
    print(request.form['message'])
    msg = False
    if request.form["username"]:
        msg = True
        send_mail(message)
    return render_template("contact.html", msg_sent=msg)


@app.route("/post/<int:num>")
def post(num):
    return render_template("post.html", r=response, n=int(num))


if __name__ == "__main__":
    app.run(debug=True)
