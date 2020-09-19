# Quick Flask webapp to host data. Should refactor in future

from flask import Flask 
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import text
import sqlite3 

# Import database functions from app_db module
from app_db import db_init

app = Flask(__name__)

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
        conn = sqlite3.connect(PACKET_DB_FILEPATH)
        return "Connected to DB OK"
    except Error as e:
        return str(e)

    

if __name__ == "__main__": 
    app.run("0.0.0.0", port=80, debug=True)
