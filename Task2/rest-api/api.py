from flask import Flask, jsonify, redirect
import json
import os

app = Flask(__name__)

# File that will we will read the scraped data
data_file = os.environ.get('DATA_FILE', '/data/scraped_data.json')

# Redirect to /data
@app.route('/', methods=['GET'])
def index():
    return redirect('/data')

# Return the scraped data
@app.route('/data', methods=['GET'])
def get_data():
    if not os.path.exists(data_file):
        return jsonify([]), 200
    with open(data_file, 'r') as f:
        data = [json.loads(line) for line in f]
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
