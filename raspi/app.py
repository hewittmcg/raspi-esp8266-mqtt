''' Flask webapp to host data received from devices ''' 

from flask import Flask, redirect, url_for, render_template

import sqlite3 

from app_db import db_init, get_nodes, get_packets

app = Flask(__name__)

NODE_DB_FILEPATH = "nodes.db"
# hardcoding nodes for testing
# nodes = [17, 18, 19]

# TODO: use an app factory for a lot of this stuff to reduce complexity/make code more readable
@app.route("/")
def index(): 
    conn = sqlite3.connect(NODE_DB_FILEPATH)
    nodes = get_nodes(conn)
    # nodes = [i[0] for i in nodes]
    conn.close()
    return render_template("index.html", nodes=nodes)
    # return redirect(url_for("list_node"))
                
@app.route("/nodes/")
def list_node(): 
    ''' Return list of all devices registered in database '''
    try:
        conn = sqlite3.connect(NODE_DB_FILEPATH)
        try: 
            db_init(conn)
        except Exception as e:
            return str(e)
        return "Connected to DB OK"
    except Exception as e:
        return str(e)

@app.route("/nodes/<node>")
def list_data(node):
    ''' Get data for the node in question '''
    conn = sqlite3.connect(NODE_DB_FILEPATH)
    packets = get_packets(conn, str(node))
    conn.close()
    return render_template("list_data.html", node=node, packets=packets)

def run(debug): 
    conn= sqlite3.connect(NODE_DB_FILEPATH)
    db_init(conn)
    conn.close()
    app.run("0.0.0.0", port=80, debug=debug)

if __name__ == "__main__": 
    app.run("0.0.0.0", port=80, debug=True)
