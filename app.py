from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)

import config
import models
import routes

load_dotenv()

if __name__ == '__main__':
    app.run()