from flask import Flask, render_template
import requests
import datetime as dt

app = Flask(__name__)

response = requests.get("https://api.npoint.io/8d8b31c3fa3510b2d111").json()

year = dt.datetime.now().year
mon = dt.datetime.today().strftime("%B")
day = dt.datetime.now().day


@app.route("/")
def home():
    return render_template("index.html", r=response, yr=year, m=mon, d=day)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:num>")
def post(num):
    return render_template("post.html", r=response, n=int(num))


if __name__ == "__main__":
    app.run(debug=True)
