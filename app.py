from flask import Flask

app = Flask(__name__, instance_path='/tmp')

import routes

app.instance_path = '/tmp'

if __name__ == '__main__':
    app.run()