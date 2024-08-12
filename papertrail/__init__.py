from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e52751703579269d27d78a5b0957e6a6'

from papertrail import routes
