from flask import Flask, request, jsonify
from db import create_redirect

app = Flask(__name__)


@app.route('/shorten', methods=['POST'])
def create_short():
    print request.data
    url = 'www.bbc.co.uk'
    hashed = hash(url)
    create_redirect(url, hashed)
    return jsonify({'redirect': hashed})


@app.route('/data', methods=['POST'])
def load_data():
    content = request.get_json(force=True)
    return jsonify(content)

if __name__ == '__main__':
    app.run(debug=True)
