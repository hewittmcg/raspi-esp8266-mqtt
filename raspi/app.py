''' Flask webapp to host data received from devices ''' 

from flask import Flask, redirect, url_for

import sqlite3 

# Import database functions from app_db module
from app_db import db_init

app = Flask(__name__)

# Path to database
NODE_DB_FILEPATH = "nodes.db"

@app.route("/")
def testdb(): 
    return redirect(url_for("list_node"))
    '''
    try: 
        conn = sqlite3.connect(PACKET_DB_FILEPATH)
        return "it works cool"
    except Error as e: 
        return str(e)
    ''' 
                
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

def run(debug): 
    app.run("0.0.0.0", port=80, debug=debug)

if __name__ == "__main__": 
    app.run("0.0.0.0", port=80, debug=True)
