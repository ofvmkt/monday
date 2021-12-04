from flask import Flask, request, abort, jsonify
import json

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    if request.method == 'POST':
        j = request.get_json(force=True)
        print(request, j)
        return "성공", 200
    else:
        abort(400)

@app.route('/')
def hello():
    
    return 'hello'

if __name__ == '__main__':
    app.run(threaded=True, port=5000)