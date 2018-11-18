# Summary

### demo/
Interactive notebooks that go into depth, with links, comments, and examples including GeoJSON/choropleths and the Walk Score API. You can click the badge to play around with the code on Google Colaboratory, but without API keys some of the live data functionality won't work.

<a href="https://colab.research.google.com/drive/14lEUPAaoI_xKydV-0M29JwBs2ArZxPXN" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

You can also view static versions on nbviewer:
* [notebook](https://nbviewer.jupyter.org/github/gotoariel/folium-demo/blob/master/demo/demo.ipynb)
* [HTML](https://nbviewer.jupyter.org/github/gotoariel/folium-demo/blob/master/demo/demo.html)

### tracker/
A barebones Flask app that demonstrates some basic Folium functionality using the WMATA API. This exact repository is hosted on Heroku [here](http://whorl.herokuapp.com). It takes one of the demo examples and shows how it can be delivered through a web browser. The code is meant to showcase possibilities, not best practices. Don't judge me.

## Environment

The project was ~~developed under Python 2.7~~ updated to Python 3.7!

* The webapp environment is specified in `requirements.txt`
	* You will need to have the `WMATA_KEY` environment variable set to your WMATA API key
* The demo environment is provided in `environment.yml`
	* You will need to put your API keys in files `demo/secrets/.wmata` and `demo/secrets/.walkscore`

You can get a [temporary guest API key](https://developer.wmata.com/Products) for WMATA.

## References

The higher level technologies used are:
* [Conda](https://conda.io/docs/) for package management
* [Git](https://git-scm.com/) for version control
* [Heroku](https://www.heroku.com) for web hosting
* [Jupyter](http://jupyter.org) for interactive Python notebooks

See the Jupyter notebook for links to documentation relevant to the demos, including Flask, Folium, and links to the APIs used.

### Heroku quickstart

Option A (*Suggested*): Use the [Python buildpack](https://github.com/heroku/heroku-buildpack-python) and deploy with Git.

Option B: If you end up needing a lot of packages or want to use Conda, you can try [deploying with Docker](https://devcenter.heroku.com/categories/deploying-with-docker).

1. Download the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and sign in with `heroku login`.
1. Create a Heroku application with `heroku create <app_name> --buildpack heroku/python` or leave the name blank to auto-generate one.
1. Make a `requirements.txt` file with all dependencies for the app.
1. Make a `runtime.txt` file that specifies the Python runtime version, eg. `python-3.7.1`.
1. Make a `Procfile` that has eg. `web: gunicorn --pythonpath . tracker --log-file=-`.
1. Deploy the repo to Heroku by `git push heroku master`. You should be able to access your app at `https://<app_name>.herokuapp.com`.

There is a [quickstart guide](https://devcenter.heroku.com/articles/getting-started-with-python) available as a reference.

#### Debugging

`heroku logs` can display remote logs from your app, however `heroku local` will run the app at `localhost:5000` and will be more useful for debugging.
* Remember to put WMATA_KEY in the environment
* The app will need to reach the public internet for geocoding

### Relevant links
* [Submarine cable map](https://submarine-cable-map-2015.telegeography.com/)
* [Color Brewer](http://colorbrewer2.org/#type=sequential&scheme=GnBu&n=9)
* [Time slider choropleth in Folium](https://nbviewer.jupyter.org/github/python-visualization/folium/blob/master/examples/TimeSliderChoropleth.ipynb)
* [US map from bodies of water](https://www.popularmechanics.com/science/a24199/gorgeous-map-united-states-bodies-of-water/)
* [US map from buildings](https://www.nytimes.com/interactive/2018/10/12/us/map-of-every-building-in-the-united-states.html)
