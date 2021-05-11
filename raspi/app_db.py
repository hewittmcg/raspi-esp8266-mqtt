''' Functions to handle db actions from Flask app '''

import sqlite3

# Constants to use to create SQL tables for nodes, packets

CREATE_NODE_TABLE_SQL = ''' CREATE TABLE IF NOT EXISTS nodes (
    device_id integer PRIMARY KEY, 
    device_name text,
    register_date text NOT NULL
); '''

CREATE_PACKET_TABLE_SQL = ''' CREATE TABLE IF NOT EXISTS packets (
    device_id integer NOT NULL,
    data integer,
    time text NOT NULL, 
    FOREIGN KEY (device_id) REFERENCES nodes (device_id)
); '''


def db_init(conn):
    ''' Initialize the database. 
    Takes in a reference to the sqlite3 connection.'''
    try: 
        conn.execute(CREATE_NODE_TABLE_SQL)
    except:
        print("Error raised during node table creation")
        raise

    try:
        conn.execute(CREATE_PACKET_TABLE_SQL) 
    except:
        print("Error raised during packet table creation")
        raise

    conn.commit()


def add_node(conn, device_id, device_name, time): 
    ''' Add a node to the node db. 
    Takes in a reference to the sqlite3 connection. '''
    # raise Exception("Function unimplemented")
    try: 
        conn.execute("INSERT INTO nodes(device_id, device_name, register_date) VALUES (?, ?, ?)", (device_id, device_name, time))
    except Exception as e:
        print("add_node(): exception raised:\n{}".format(e))

    conn.commit()

def add_packet(conn, data, time, device_id):
    ''' Add a packet to the database.
    Takes in a reference to the sqlite3 connection, the 
    packet data, the time the packet was received, and the 
    device id the packet was received from. '''
    # raise Exception("Function unimplemented")
    print("Adding packet device_id: {} data {} time {}".format(device_id, data, time))
    try: 
        conn.execute("INSERT INTO packets (device_id, data, time) VALUES (?, ?, ?)", (device_id, data, time))
    except Exception as e:
        print("add_packet(): exception raised:\n{}".format(e))

    conn.commit()

def get_nodes(conn):
    ''' Return a list of all the nodes in the database. '''
    try:
        nodes = (conn.execute("SELECT * FROM nodes")).fetchall()
    except Exception as e:
        print("get_nodes(): exception raised:\n{}".format(e))
    return nodes

def get_packets(conn, device_id):
    ''' Return a list of all the packets associated with the given device id '''
    try:
        packets = (conn.execute("SELECT * FROM packets WHERE device_id = (?)", (device_id))).fetchall()
    except Exception as e:
        print("get_packets(): exception raised:\n{}".format(e))
    return packets

def device_exists(conn, device_id):
    raise Exception("Function unimplemented")

        
