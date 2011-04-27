#!/usr/bin/python
# -*- coding: utf-8 -*-

import pywapi

import cgitb
cgitb.enable()


# Get the current conditions for the given station.
noaa = pywapi.get_weather_from_noaa('KARR')
yahoo = pywapi.get_weather_from_yahoo('60502', '')

# The Yahoo pressure dictionary.
ypressure = {'0': 'steady', '1': 'rising', '2': 'falling'}

# Check for gusts.
try:
  gust = ', gusting to %s mph' % noaa['wind_gust_mph']
except KeyError:
  gust = ''
  
# The forecasts.
today = yahoo['forecasts'][0]
tomorrow = yahoo['forecasts'][1]

# The content.
content = '''Content-type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<meta name="viewport" content = "width = device-width" />
<title>Weather</title>
<style type="text/css">
  body { font-family: Helvetica;}
  h1 { font-size: 125%%;}
</style>
</head>
<body>
<h1>Temperature: %.0f&deg;</h1>
<p>%s<br />
Wind: %s at %s mph%s<br />''' % (float(noaa['temp_f']), yahoo['condition']['text'], noaa['wind_dir'], noaa['wind_mph'], gust )

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

content += '<p><img width="75%" src="http://i.imwx.com/web/radar/us_ord_ultraradar_plus_usen.jpg" /></p>\n'

content += '''<h1>Today</h1>
<p>High: %s&deg;<br />
Low: %s&deg;<br />
%s</p>
''' % (int(today['high']), int(today['low']), today['text'])

content += '''<h1>Tomorrow</h1>
<p>High: %s&deg;<br />
Low: %s&deg;<br />
%s</p>
''' % (int(tomorrow['high']), int(tomorrow['low']), tomorrow['text'])

content += '''</body>
</html>'''

print content.encode('utf8')

