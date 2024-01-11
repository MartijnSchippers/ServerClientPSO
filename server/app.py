from flask import Flask
from server import Application


application = Application()

# if __name__ == '__main__':
app = Flask(__name__)
application.define_routes(app)
