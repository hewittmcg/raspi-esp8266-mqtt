''' Flask webapp to host data received from devices '''

from flask import Flask, redirect, url_for, render_template, jsonify
from flask_cors import CORS

import sqlite3
import os
from app_db import db_init, get_nodes, get_packets

app = Flask(__name__)

# enable cross-origin requests
CORS(app, resources={r'/*': {'origins': '*'}})

dirname = os.path.dirname(__file__)
NODE_DB_FILEPATH = os.path.join(dirname, "nodes.db")

# TODO: use an app factory for a lot of this stuff to reduce complexity/make code more readable

@app.route("/devices", methods = ["GET"])
def list_devices():
    conn = sqlite3.connect(NODE_DB_FILEPATH)
    nodes = get_nodes(conn)
    conn.close()
    return jsonify(nodes)

@app.route("/device/<device>", methods = ["GET"])
def list_packets(device):
    conn = sqlite3.connect(NODE_DB_FILEPATH)
    packets = get_packets(conn, str(device))
    conn.close()
    return jsonify(packets)    

def run(debug):
    conn = sqlite3.connect(NODE_DB_FILEPATH)
    db_init(conn)
    conn.close()
    app.run("0.0.0.0", port=5000, debug=debug)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
