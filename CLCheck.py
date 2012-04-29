#!/usr/bin/env python
import requests
import random
import sys
import json
import os
from bs4 import BeautifulSoup

path = os.path.dirname(os.path.realpath(__file__))
lastfile = os.path.join(path,'last')
def format_push(p):
    desc = p.text[p.text.find('-') + 2:p.text.rfind('-')]
    href = p.find('a').get('href')
    push = {'email':'boxcar@egd.im',
    'notification[from_screen_name]':'CL',
    'notification[message]':desc,
    'notification[source_url]':href,
    'notification[icon_url]':'http://egd.im/bot/clicon.png'}
    return push

def send_push(push):
    url = "http://boxcar.io/devices/providers/X5RCfRKbUoblfOfcbAMH/notifications"
    r = requests.post(url, data=push)

with open(lastfile) as r: last = json.load(r)
hi = random.randint(1700,1705)#VOODOO!
lo = random.randint(1095,1100)#VOODOO!
r = requests.get("http://sfbay.craigslist.org/search/apa/eby?query=&srchType=A&minAsk=%i&maxAsk=%i&bedrooms=2&nh=48&nh=49" % (lo,hi))
#x = etree.parse(r.content, etree.HTMLParser())
soup = BeautifulSoup(r.content)
newlast = []
for p in soup.findAll('p')[:10]: # last 10 only.
    a = p.find('a')
    if a.get('href') in last: break
    push = format_push(p)
    send_push(push)
    if len(newlast) < 5:
        newlast.append(a.get('href'))
newlast.extend(last)
newlast = newlast[:5]
with open(lastfile,'w') as w: json.dump(newlast,w)
