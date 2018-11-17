import requests
import folium
import geocoder
import string
import os

from ediblepickle import checkpoint
from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # prevents browser caching maps
app.vars = {}

@app.route('/')
def main():
  return redirect('/index.html')

@app.route('/index.html', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('input.html')
  elif request.method == 'POST':
    app.vars['location'] = request.form['location']
    app.vars['radius'] = request.form['radius']
    # app.vars['route'] = request.form.get('route')
    app.vars['cache'] = request.form.get('cache')
    app.vars['map_path'] = f"maps/map-{app.vars['location']}-{app.vars['radius']}.html"
    return redirect('/tracker.html')

@app.route('/maps/map.html')
def show_map():
  map_path = app.vars.get("map_path")
  return send_file(os.path.join(app.root_path, map_path))

@app.route('/tracker.html')
def tracker():
  loc = geocoder.osm(app.vars['location'])
  if loc.lat is not None and loc.lng is not None:
    latlng = [loc.lat, loc.lng]
  else:
    return redirect('/geoerror.html')
  
  map_path = app.vars.get("map_path")
  if app.vars.get("cache") == "yes" and os.path.isfile(os.path.join(app.root_path, map_path)):
    return render_template('display.html')
  else:
    bus_map = folium.Map(location=latlng, zoom_start=15)
    bus_map.add_child(folium.Marker(location=latlng,
                                  popup=loc.address,
                                  icon=folium.Icon(color='blue')))

    # Call API for bus locations

    bus_list = get_buses(loc.lat, loc.lng, app.vars['radius'])

    for bus in bus_list:
      folium.features.RegularPolygonMarker(location = [bus['Lat'], bus['Lon']],
                                           popup = 'Route %s to %s' % (bus['RouteID'], bus['TripHeadsign']),
                                           number_of_sides = 3,
                                           radius = 15,
                                           weight = 1,
                                           fill_opacity = 0.8,
                                           rotation = 30).add_to(bus_map)
  
    bus_map.save(os.path.join(app.root_path, map_path))
    return render_template('display.html')
  pass

def get_buses(lat, lon, radius):
  """
  All values passed as strings and radius in meters
  """
  headers = {'api_key': os.environ['WMATA_KEY']}

  session = requests.Session()
  session.mount('https://api.wmata.com',
                requests.adapters.HTTPAdapter(max_retries = 2))

  bus_endpoint = 'https://api.wmata.com/Bus.svc/json/jBusPositions'
  
  params = {'Lat': lat,
            'Lon': lon,
            'Radius': radius}

  # if app.vars['route']:
  #   params['RouteID'] = app.vars['route']

  response = session.get(bus_endpoint, params = params, headers = headers)
  if not response.status_code == 200:
    return redirect('/apierror.html')
  else:
    return response.json()['BusPositions']

@app.route('/apierror.html')
def apierror():
  details = "There was an error with one of the API calls you attempted."
  return render_template('error.html', culprit='API', details=details)

@app.route('/geoerror.html')
def geoerror():
  details = "There was a problem getting coordinates for the location you requested."
  return render_template('error.html', culprit='Geocoder', details=details)


if __name__ == '__main__':
  app.run(host='0.0.0.0')
