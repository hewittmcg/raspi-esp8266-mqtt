''' Functions to handle db actions from Flask app '''

import sqlite3

# Constants to use to create SQL tables for nodes, packets

CREATE_NODE_TABLE_SQL = ''' CREATE TABLE IF NOT EXISTS nodes (
    device_id integer PRIMARY KEY, 
    device_name text,
    register_date text NOT NULL
); '''

CREATE_PACKET_TABLE_SQL = ''' CREATE TABLE IF NOT EXISTS packets (
    data integer,
    time text NOT NULL, 
    FOREIGN KEY (device_id) REFERENCES nodes (device_id)
); '''


def db_init(conn):
    ''' Initialize the database. 
    Takes in a reference to the sqlite3 connection.
    Returns this reference to allow chaining if desired. '''
    try: 
        conn.execute(CREATE_NODE_TABLE_SQL)
    except Error as e:
        print("Error raised during node table creation")
        raise

    try:
        conn.execute(CREATE_PACKET_TABLE_SQL) 
    except Error as e:
        print("Error raise during packet table creation")
        raise

    return conn 


def add_node(conn, device_id, device_name): 
    ''' Add a node to the node db. 
    Takes in a reference to the sqlite3 connection. '''
    raise Exception("Function unimplemented")
    try: 
        conn.execute("INSERT INTO nodes(device_id, device_name) VALUES (?, ?)", device_id, device_name)

def add_packet(conn, data, time, device_id):
    ''' Add a packet to the database.
    Takes in a reference to the sqlite3 connection, the 
    packet data, the time the packet was received, and the 
    device id the packet was received from. '''
    raise Exception("Function unimplemented")