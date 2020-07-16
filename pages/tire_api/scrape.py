

for relev in tire_urls:
    r = requests.get(relev, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}).text
    regex = re.compile(r'\/buy-tires\/[a-zA-Z0-9\-]*\?', re.M)
    tire_l.append(regex.findall(r))

for relev in wheel_urls:
    r = requests.get(relev, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}).text
    regex = re.compile(r'\/buy-wheels\/[a-zA-Z0-9\-]*\?', re.M)
    wheel_l.append(regex.findall(r))
