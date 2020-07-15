import requests_html
from lxml import html
from lxml import etree

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
    "https://www.discounttire.com/wheels/atv-utv-catalog?q=%3AbestSeller-asc&page=0",
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
https://stackoverflow.com/a/58016225/9295513
When this is done testing, it will be wrapped up in a loop for every url in question
The relevant link will be shown to the customer to explore the further pages\
	because I don't know how to "inject" a click.
"""

relev = wheel_urls[len(wheel_urls) - 1]
session = requests_html.HTMLSession()
r = session.get(relev)

doc = etree.HTML(r.content)
links = []
for url in doc.xpath('//a[@href]'):
    links.append(url.get('href'))
for i in links:
    print(i)
