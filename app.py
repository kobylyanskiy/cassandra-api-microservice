import json
from flask import Flask, request
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement, dict_factory
import cassandra

def cassandra_connection():
    clusterr = cassandra.cluster.Cluster([
        'cassandra-0.cassandra.default.svc.cluster.local',
        'cassandra-1.cassandra.default.svc.cluster.local',
        'cassandra-2.cassandra.default.svc.cluster.local'
    ])
    return clusterr.connect()

cass_app = Flask(__name__)
session = cassandra_connection()

session.execute("""
        CREATE KEYSPACE IF NOT EXISTS operations
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """)

session.set_keyspace('operations')

session.row_factory = dict_factory

@cass_app.route('/operations', methods=['GET', 'POST'])
def operations():
    if request.method == 'POST':
        operation = request.get_json(force=True)
        print(operation)


        query = SimpleStatement(
        """
        INSERT INTO operation(codename, location, date_start, date_end,
        operation_type, difficulty, status, costs, agents, target)
        VALUES (%(codename)s, %(location)s, %(date_start)s, %(date_end)s, %(operation_type)s, %(difficulty)s, %(status)s, %(costs)s, %(agents)s, %(target)s)
        """)
        try:
            session.execute(query,operation)    
            return json.dumps({
                'result': True,
            })
        except Exception:
            return json.dumps({
                'result': False,
                'error_msg' : 'Insert operation went wrong, check the arguments'
            })            
    else:
        result = {}
        try:
            rows = session.execute("SELECT * FROM operation")
            for user_row in rows:
                result[user_row['codename']] = user_row    
            return json.dumps(result)
        except Exception:
            return json.dumps({
                'result': False,
                'error_msg' : 'It is a DB problem, check the operation table'
            })   


@cass_app.route('/operations/<string:codename>', methods=['GET', 'POST'])
def get_agent(codename):
    if request.method == 'POST':
        operation = request.get_json(force=True)
        print(operation)
        try:        
            session.execute(
            """
            UPDATE operation
            SET date_end = %s, status = %s, costs = %s
            WHERE codename = %s
            """,
            (operation['date_end'], operation['status'], operation['costs'], codename)
            )
            return json.dumps({
                'result': True,
            })
        except Exception:
            return json.dumps({
                'result': False,
                'error_msg' : 'Update operation went wrong, check the arguments'                
            })
    else:
        print(codename)
        try:
            row = session.execute(
            """
            SELECT * FROM operation
            WHERE codename = %s 
            """, 
            (codename,)
            )
            return json.dumps(row[0])
        except Exception:
            return json.dumps({
                'result': False,
                'error_msg' : 'Select operation went wrong, check the operation codename'                
            })            





if __name__ == '__main__':
    session.execute("""
        CREATE TABLE operation(
            codename text,
            location text,
            date_start text,
            date_end text,
            operation_type text,
            difficulty int,
            status text,
            costs int,
            agents list<text>,
            target list<text>,
            PRIMARY KEY (codename))
        """)
    cass_app.run(host='0.0.0.0', port=5000)
