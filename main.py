from flask import Flask, jsonify, request
import ldclient
from ldclient.config import Config
from ldclient import Context
from source.helper import init_LD_client, generate_results

app = Flask(__name__)

# In-memory storage for Metrics, Percentages, SDK Key, and Flag Key
data_store = {
    "metrics": [],
    "percentages": [],
    "sdk_key": None,
    "flag_key": None
}

@app.route('/add_keys', methods=['POST'])
def add_keys():
    content = request.json
    sdk_key = content.get('sdk_key')
    flag_key = content.get('flag_key')

    data_store["sdk_key"] = sdk_key
    data_store["flag_key"] = flag_key

    init_LD_client(sdk_key)
    
    return jsonify({"message": "Client Initialized successfully", "data": data_store}), 200

@app.route('/add', methods=['POST'])
def add_entry():
    content = request.json
    metrics = content.get('metrics')
    percentages = content.get('percentages')

    if not isinstance(metrics, list) or not isinstance(percentages, list):
        return jsonify({"error": "Both metrics and percentages should be lists."}), 400

    data_store["metrics"].extend(metrics)
    data_store["percentages"].extend(percentages)

    result = generate_results(data_store)

    if result:
        return jsonify({"message": "Generated Results Successfully", "data": data_store}), 200


@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_store), 200

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)