import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Web App with Python Flask!'

if __name__ == '__main__':
    app.run()