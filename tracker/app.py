import requests
import folium
import geocoder
import string
import os
import json
from functools import wraps, update_wrapper
from datetime import datetime
from pathlib import Path

from ediblepickle import checkpoint
from flask import Flask, render_template, request, redirect, url_for, send_file, make_response


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.vars = {}

def escape_apostrophes(string):
  return string.replace(r"'", r"\'")

def escape_spaces(string):
  return string.replace(" ", "_")

def nocache(view):
  @wraps(view)
  def no_cache(*args, **kwargs):
    response = make_response(view(*args, **kwargs))
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
        
  return update_wrapper(no_cache, view)

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
    escaped_location = escape_spaces(app.vars['location'])
    map_name = f"map-{escaped_location}-{app.vars['radius']}.html"
    app.vars['map_path'] = os.path.join(app.root_path, 'maps/' + map_name)
    return redirect('/tracker.html')

@app.route('/maps/map.html')
@nocache
def show_map():
  map_path = app.vars.get("map_path")
  map_file = Path(map_path)
  if map_file.exists():
    return send_file(map_path)
  else:
    return render_template('error.html', culprit='map file', details="the map file couldn't be loaded")

@app.route('/tracker.html')
def tracker():
  loc = geocoder.osm(app.vars.get('location'))
  if loc.lat is not None and loc.lng is not None:
    latlng = [loc.lat, loc.lng]
  else:
    return redirect('/geoerror.html')
  
  # insist on a valid map config
  map_path = app.vars.get("map_path")
  if not map_path:
    return redirect('/error.html')
  if app.vars.get("cache") == "yes" and Path(map_path).exists():
    return render_template('display.html')
  else:
    bus_map = folium.Map(location=latlng, zoom_start=15)
    bus_map.add_child(folium.Marker(location=latlng,
                                    popup=escape_apostrophes(loc.address),
                                    icon=folium.Icon(color='blue')))

    # Call API for bus locations
    bus_list = get_buses(loc.lat, loc.lng, app.vars['radius'])

    for bus in bus_list:
      route_id = bus.get('RouteID')
      trip_headsign = escape_apostrophes(bus.get('TripHeadsign'))
      folium.features.RegularPolygonMarker(location = [bus['Lat'], bus['Lon']],
                                           popup = f"Route {route_id} to {trip_headsign}",
                                           number_of_sides = 3,
                                           radius = 15,
                                           weight = 1,
                                           fill_opacity = 0.8,
                                           rotation = 30).add_to(bus_map)
  
    bus_map.save(map_path)
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

@app.route('/error.html')
def error():
  details = "There was some kind of error."
  return render_template('error.html', culprit='logic', details=details)

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
