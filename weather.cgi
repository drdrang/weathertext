#!/usr/bin/python
# -*- coding: utf-8 -*-

# These are the items that can be customized for a different location.
# The zipcode is just the 5-digit code; no need for extensions.
# The station can be found by going to 
#   http://www.weather.gov/xml/current_obs/seek.php?state=il&Find=Find
# and choosing the closest NOAA station for your state.
# The radar image can be found at http://weather.com by searching
# on your location and then following the "Classic Map" link. Use
# the URL of that image here.
zipcode = '60502'
station = 'KARR'
radar   = 'http://i.imwx.com/web/radar/us_ord_ultraradar_plus_usen.jpg'


# The code below shouldn't be modified unless you want to change the layout
# or the type of data presented.

import pywapi
import datetime
import re

import cgitb
cgitb.enable()

# The date and time as a string. Note: My host's server is on Eastern Time
# and I'm on Central Time, so I subtract an hour.
now = datetime.datetime.now() - datetime.timedelta(hours=1)
now = now.strftime("%a, %b %d %I:%M %p")
# Delete leading zeros for day and hour.
now = re.sub(r' 0(\d )', r' \1', now)   # day has a space before and after
now = re.sub(r'0(\d:)', r'\1', now)     # hour has a colon after

# The date as a string. This is for comparison with forecast dates.
today = datetime.datetime.now() - datetime.timedelta(hours=1)
today = today.strftime("%d %b %Y")
today = re.sub(r'^0(\d)', r'\1', today)   # delete leading zero on day


# Get the current conditions for the given station.
noaa = pywapi.get_weather_from_noaa(station)
yahoo = pywapi.get_weather_from_yahoo(zipcode, '')

# Interpretation of the Yahoo pressure dictionary.
ypressure = {'0': 'steady', '1': 'rising', '2': 'falling'}

  
# The forecasts
f1 = yahoo['forecasts'][0]
f2 = yahoo['forecasts'][1]
if f1['date'] == today:
  f1str = 'Today'
  f2str = 'Tomorrow'
else:
  f1str = 'Tomorrow'
  f2str = 'Next day'

# Assemble the content,.
content = '''Content-type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<meta name="viewport" content = "width = device-width" />
<title>Weather - %s</title>
<style type="text/css">
  body { font-family: Helvetica; }
  h1 { font-size: 175%%;
    text-align: center;
    margin-bottom: 0; }
  h2 { font-size: 125%%;
    margin-top: 0;
    margin-bottom: 0; }
  #now { margin-left: 0; }
  #gust { padding-left: 2.75em; }
  div p { margin-top: .25em;
    margin-left: .25em; }
</style>
</head>
<body onload="setTimeout(function() { window.top.scrollTo(0, 1) }, 100);">
<h1>%.0f&deg; &bull; %s </h1>''' % (now, float(noaa['temp_f']), yahoo['condition']['text'])

content += '<p><img width="100%%" src="%s" /></p>\n' % radar

content += '<p id="now">Wind: %s at %s mph<br />' % (noaa['wind_dir'], noaa['wind_mph'] )

try:
  content += '<span id="gust">Gusting to %s mph</span><br />\n' % noaa['wind_gust_mph']
except KeyError:
  pass

try:
  content += 'Wind Chill: %s&deg;<br />\n' % noaa['windchill_f']
except KeyError:
  pass

content += 'Relative Humidity: %s%%<br />\n' % noaa['relative_humidity']

try:
  content += 'Heat Index: %s&deg;<br />\n' % noaa['heat_index_f']
except KeyError:
  pass

content += 'Pressure: %s and %s<br />\n' % (float(yahoo['atmosphere']['pressure']), ypressure[yahoo['atmosphere']['rising']])

content += 'Sunlight: %s to %s</p>\n' % (yahoo['astronomy']['sunrise'], yahoo['astronomy']['sunset'])

content += '''<div id="f1"><h2>%s</h2>
<p>High: %s&deg;<br />
Low: %s&deg;<br />
%s</p></div>
''' % (f1str, int(f1['high']), int(f1['low']), f1['text'])

content += '''<div id="f2"><h2>%s</h2>
<p>High: %s&deg;<br />
Low: %s&deg;<br />
%s</p></div>
''' % (f2str, int(f2['high']), int(f2['low']), f2['text'])

content += '''</body>
</html>'''

print content.encode('utf8')

