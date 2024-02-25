# File: app.py      
# Date: 13-01-24     
# Description: This script starts the server application. Type 'flask run --host=0.0.0.0' in the terminal to start. 
#   Change the settings in 'settings.json' before a run. Obtain the results in 'results.json' and run 'graph_results.py'
# Author: Martijn Schippers

from flask import Flask
from server import Application


application = Application()

# if __name__ == '__main__':
app = Flask(__name__)
application.define_routes(app)
