import requests
import re
from Flask import Flask, render_template


def get_urls():
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

    tire_l = []
    wheel_l = []

    # """
    for relev in tire_urls:
        r = requests.get(relev, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}).text
        regex = re.compile(r'\/buy-tires\/[a-zA-Z0-9\-]*\?', re.M)
        tire_l += regex.findall(r)

    for relev in wheel_urls:
        r = requests.get(relev, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}).text
        regex = re.compile(r'\/buy-wheels\/[a-zA-Z0-9\-]*\?', re.M)
        wheel_l += regex.findall(r)
    # """

    tire_l = ["https://www.discounttire.com" + i for i in tire_l]
    wheel_l = ["https://www.discounttire.com" + i for i in wheel_l]

    return (tire_l, wheel_l)


@app.route("/tires.html")
def tires():
    tires = get_urls()[0]
    return render_template("tires.html", tires=tires)


@app.route("/wheels.html")
def wheels():
    wheels = get_urls()[1]
    return render_template("wheels.html", wheels=wheels)
