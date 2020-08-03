/*
Got help from:
https://chat.stackoverflow.com/transcript/message/49944633#49944633
https://chat.stackoverflow.com/transcript/message/49946525#49946525
https://stackoverflow.com/a/6375580/9295513
https://stackoverflow.com/questions/6375461/get-html-code-using-javascript-with-a-url
https://stackoverflow.com/a/32604544/9295513
https://stackoverflow.com/questions/53309569/async-await-func-doesnt-wait-to-console-log-its-response/53309593
https://chat.stackoverflow.com/transcript/message/50075243#50075243

This was originally written in Python; the relevant loop went
for relev in tire_urls:
    r = requests.get(relev, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}).text
    regex = re.compile(r'\/buy-tires\/[a-zA-Z0-9\-]*\?', re.M)
    tire_l.append(regex.findall(r))
*/

const { promises } = require('dns');
const fetch = require('node-fetch');

const tire_urls = [
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
];

const wheel_urls = [
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
];

function getter_helper(urls) {
	const lst = [];

	urls.forEach(url => {
		const request = fetch(url).then(function (response) {
			return response.text();
		})
		lst.push(request);
	})

	return Promise.all(lst);
}

function getWheel() {
	var wheel_l = [];
	wheel_urls.forEach(i => {
		var r = new XMLHttpRequest();
		r.open("GET", i, true);
		r.send(null);
		r.onreadystatechange = function () {
			if (r.readyState == 4) {
				const re = new RegExp("\/buy-wheels\/[a-zA-Z0-9\-]*\?");
				wheel_l.concat([...r.responseText.matchAll(re)]);
			}
		}
	});
	return wheel_l;
}


function getTire() {
	var tire_l = [];
	tire_urls.forEach(function (i) {
		var r = new XMLHttpRequest();
		r.open("GET", i, true);
		r.send(null);
		r.onreadystatechange = function () {
			if (r.readyState == 4) {
				var re = new RegExp("\/buy-tires\/[a-zA-Z0-9\-]*\?");
				tire_l.push.apply(tire_l, ["yes", "no", "maybe"]); //re.exec(r.responseText)
			}
		}
	});
	tire_l.push.apply(tire_l, ["yes", "no", "maybe"]);
	return tire_l;
}

async function getCircle(regex, urls) {
	var processed = [];
	const re = RegExp(regex, "gm");
	const text = await getter_helper(urls);
	text.forEach(t => {
		processed.push([...t.match(re)]);
	});
	return processed;
}

getCircle("\/buy-wheels\/[a-zA-Z0-9\-]*\?", wheel_urls).then(j => console.log(j.flatMap(x => x.map(y => "https://www.discounttire.com" + y[0]))));

module.exports.getCircle = getCircle;
