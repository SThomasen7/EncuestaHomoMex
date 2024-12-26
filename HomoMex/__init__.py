"""Package Initializer"""
import flask

app = flask.Flask(__name__)
app.config.from_object("HomoMex.config")
app.config.from_envvar('HOMOMEX_SETTINGS', silent=True)

import HomoMex.views
import HomoMex.model
