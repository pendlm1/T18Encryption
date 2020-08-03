import requests
import re
from flask import Flask, render_template, url_for
import os

tire_urls = [
    "https://www.discounttire.com/tires/all-season-catalog",
    "https://www.discounttire.com/tires/all-terrain-catalog",
    "https://www.discounttire.com/tires/atv-utv-catalog",
    "https://www.discounttire.com/tires/competition-catalog",
    "https://www.discounttire.com/tires/lawn-catalog",
    "https://www.discounttire.com/tires/mud-terrain-catalog",
    "https://www.discounttire.com/tires/passenger-catalog",
    "https://www.discounttire.com/tires/performance-catalog",
    "https://www.discounttire.com/tires/spare-catalog",
    "https://www.discounttire.com/tires/summer-catalog",
    "https://www.discounttire.com/tires/touring-catalog",
    "https://www.discounttire.com/tires/trailer-catalog",
    "https://www.discounttire.com/tires/truck-catalog",
    "https://www.discounttire.com/tires/winter-catalog"
]

wheel_urls = [
    "https://www.discounttire.com/wheels/atv-utv-catalog",
    "https://www.discounttire.com/wheels/chrome-catalog",
    "https://www.discounttire.com/wheels/machined-catalog",
    "https://www.discounttire.com/wheels/mesh-catalog",
    "https://www.discounttire.com/wheels/modular-catalog",
    "https://www.discounttire.com/wheels/multi-spoke-catalog",
    "https://www.discounttire.com/wheels/painted-catalog",
    "https://www.discounttire.com/wheels/passenger-catalog",
    "https://www.discounttire.com/wheels/split-spoke-catalog",
    "https://www.discounttire.com/wheels/split-spoke-catalog",
    "https://www.discounttire.com/wheels/truck-catalog"
]


def get_urls(urls, reg_ex):

    url_list = []

    for relev in urls:
        r = requests.get(relev, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}).text  # This header had to be taken from elsewhere because some ID needs to be given, and I don't know how to give my own.
        regex = re.compile(reg_ex, re.M)
        url_list += regex.findall(r)

    url_list = ["https://www.discounttire.com" + i for i in url_list]

    return url_list


def name_url(s):
    s = s[11:len(s)-1]
    s = s.split("-")
    s = [i.title() for i in s]
    s = " ".join(s)
    return s


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/coupons')
def coupons():
    return render_template("coupons.html")


@app.route('/location')
def location():
    return render_template("location.html")


@app.route('/repairs')
def repairs():
    return render_template("repairs.html")


@app.route('/reviews')
def reviews():
    return render_template("reviews.html")


@app.route("/shop")
def shop():
    return render_template("shop.html")


@app.route("/tire_api", methods=['GET', 'POST'])
def tires():
    tires = get_urls(tire_urls, r'\/buy-tires\/[a-zA-Z0-9\-]*\?')
    tire_names = [name_url(i) for i in tires]
    return render_template(url_for("tire_api/tires.html"), tires=(tires, tire_names))


@app.route("/tire_api/wheels.html", methods=['GET', 'POST'])
def wheels():
    wheels = get_urls(wheel_urls, r'\/buy-wheels\/[a-zA-Z0-9\-]*\?')
    wheel_names = [name_url(i) for i in wheels]
    return render_template(url_for("tire_api/wheels"), wheels=(wheels, wheel_names))


if __name__ == '__main__':
    app.run(debug=True)
