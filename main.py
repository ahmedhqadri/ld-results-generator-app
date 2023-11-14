from flask import Flask, jsonify, request
import ldclient
from ldclient import Stage
from ldclient.config import Config
from ldclient import Context
from source.helper import init_LD_client, generate_results, migration_builder, create_multi_context
import time
import random
import threading

app = Flask(__name__)

# In-memory storage for Metrics, Percentages, SDK Key, and Flag Key
data_store = {
    "metrics": [],
    "percentages": [],
    "sdk_key": None,
    "flag_key": None,
    "migration_running": False
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

def long_running_task():

    migrator = migration_builder()
    default_stage = Stage.OFF
    flag_key = data_store["flag_key"]
    data_store["migration_running"] = True

    while data_store["migration_running"]:
        context = create_multi_context()
        # Out of 1000 reads, how many will fail
        read_error_rates = {
            "old": random.randint(20,40),
            "new": random.randint(5,20)
            }

        # Out of 1000 writes, how many will fail
        write_error_rates = {
            "old": random.randint(10,30),
            "new": random.randint(5,20)
            }
        
        read_result = migrator.read(flag_key, context, default_stage, read_error_rates)
        write_result = migrator.write(flag_key, context, default_stage, write_error_rates)
        

@app.route('/start_migration', methods=['POST'])
def start_migration():
    if not data_store["migration_running"]:
        thread = threading.Thread(target=long_running_task)
        thread.start()
        return jsonify({"message": "Migration started"}), 200
    else:
        return jsonify({"error": "Migration is already running"}), 400

@app.route('/stop_migration', methods=['POST'])
def stop_migration():
    data_store["migration_running"] = False
    return jsonify({"message": "Migration stopped"}), 200

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_store), 200

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)