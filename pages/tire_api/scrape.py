import requests
import re

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

"""
Got help from:
https://chat.stackoverflow.com/transcript/message/49944633#49944633
https://chat.stackoverflow.com/transcript/message/49946525#49946525

When this is done testing, it will be wrapped up in a loop for every url in question
The relevant link will be shown to the customer to explore the further pages\
	because I don't know how to "inject" a click.
"""

tire_l = []
wheel_l

for relev in tire_urls:
    r = requests.get(relev, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}).text
    regex = re.compile(r'\/buy-tires\/[a-zA-Z0-9\-]*\??', re.M)
    tire_l.append(regex.findall(r))

for relev in wheel_urls:
    r = requests.get(relev, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}).text
    regex = re.compile(r'\/buy-wheels\/[a-zA-Z0-9\-]*\??', re.M)
    wheel_l.append(regex.findall(r))
