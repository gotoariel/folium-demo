# Summary

A barebones Flask app that demonstrates some basic Folium functionality using the WMATA API. This exact repository is hosted on Heroku [here](http://whorl.herokuapp.com).

The core of this demo is the Jupyter notebook (`demo.ipynb`). It goes into depth, with links, comments, and examples including GeoJSON/choropleths and the Walk Score API. An HTML version of the notebook is available as `demo.html`.

The rest of the repo takes one of those examples and shows how it can be delivered through a web browser. The code is meant to showcase possibilities, not best practices. Don't judge me.

## Environment

The project was ~~developed under Python 2.7~~ updated to Python 3.7!

An environment is provided in `environment.yml`. Using Conda you can run `conda env create -f environment.yml` to create a virtual environment with all the dependencies for both the Flask app and Jupyter notebook.

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
1. Make a `runtime.txt` file that specifies the Python runtime version, eg. `python-3.7.0`.
1. Make a `Procfile` that has eg. `web: gunicorn --pythonpath . tracker --log-file=-`.
1. Deploy the repo to Heroku by `git push heroku master`. You should be able to access your app at `https://<app_name>.herokuapp.com`.

There is a [quickstart guide](https://devcenter.heroku.com/articles/getting-started-with-python) available as a reference.

## Debugging

You can run Flask apps locally by eg. `python app.py`. This app will run at `localhost:33507`.

`heroku logs` can display remote logs from your app, however `heroku local` will run the app at `localhost:5000` and will be more useful for debugging.
