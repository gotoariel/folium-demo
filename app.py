import requests
import folium
import geocoder
import string
import os

from ediblepickle import checkpoint
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.vars = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('input.html')
  elif request.method == 'POST':
    app.vars['location'] = request.form['location']
    app.vars['radius'] = request.form['radius']
    app.vars['cache'] = request.form.get('cache')
    return redirect('/tracker')

@app.route('/tracker')
def tracker():

  loc = geocoder.google(app.vars['location'])
  bus_map = folium.Map(location=loc.latlng, zoom_start=15)
  bus_map.add_child(folium.Marker(location=loc.latlng,
                                  popup=loc.address,
                                  icon=folium.Icon(color='blue')))

  # Call API for bus locations

  app.vars['refresh'] = False if app.vars['cache'] == 'yes' else True
  bus_list = get_buses(loc.lat, loc.lng, app.vars['radius'])

  for bus in bus_list:
    folium.features.RegularPolygonMarker(location = [bus['Lat'], bus['Lon']],
                                         popup = 'Route %s to %s' % (bus['RouteID'], bus['TripHeadsign']),
                                         number_of_sides = 3,
                                         radius = 10,
                                         weight = 1,
                                         fill_opacity = 0.8,
                                         rotation = 30).add_to(bus_map)
  bus_map.save('templates/map.html') 
  
  return render_template('map.html')

@checkpoint(key = string.Template('{0}x{1}_radius{2}.buslist'),
            work_dir = 'cache/',
            refresh = lambda: app.vars.get('refresh', False))
def get_buses(lat, lon, radius):
  """
  All values passed as strings and radius in meters
  """
  headers = {'api_key': os.environ['API_KEY']}

  session = requests.Session()
  session.mount('https://api.wmata.com',
                requests.adapters.HTTPAdapter(max_retries = 2))

  bus_endpoint = 'https://api.wmata.com/Bus.svc/json/jBusPositions'
  params = {'Lat': lat,
            'Lon': lon,
            'Radius': radius}

  response = session.get(bus_endpoint, params = params, headers = headers)
  if not response.status_code == 200:
    return redirect('/error')
  else:
    return response.json()['BusPositions']

@app.route('/error')
def error():
  details = "There was an error with one of the API calls you attempted."
  return render_template('error.html', culprit='API', details=details)

if __name__ == '__main__':
  urls = []
  app.run(port=33507)
  for rule in app.url_map.iter_rules():
    urls.append(url_for(rule.endpoint))
  print urls
