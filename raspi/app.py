''' Flask webapp to host data received from devices ''' 

from flask import Flask, redirect, url_for, render_template

import sqlite3 

from app_db import db_init

app = Flask(__name__)

NODE_DB_FILEPATH = "nodes.db"
# hardcoding nodes for testing
nodes = [17, 18, 19]

@app.route("/")
def index(): 
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
    return render_template("list_data.html", node=18, data=["test", "test test"])

def run(debug): 
    app.run("0.0.0.0", port=80, debug=debug)

if __name__ == "__main__": 
    app.run("0.0.0.0", port=80, debug=True)
