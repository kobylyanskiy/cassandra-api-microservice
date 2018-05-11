import json
from flask import Flask, request
from cassandra.query import SimpleStatement
from cassandra.cluster import Cluster


app = Flask(__name__)


def cassandra_connection():
    cluster = Cluster(['cassandra-0.cassandra.default.svc.cluster.local'])
    return cluster.connect()


@app.route('/operations', methods=['GET', 'POST'])
def operations():
    if request.method == 'POST':
        operation = request.get_json(silent=True)
        print(operation)
        return json.dumps({
            'result': True,
        })
    else:
        return json.dumps({
            'result': True,
            'data': [],
        })


@app.route('/operation/<string:codename>', methods=['GET'])
def get_agent(codename):
    return json.dumps({
        'result': True,
        'operation': {'codename': 'codename'}
    })


sess = cassandra_connection()
sess.execute(
    """
    CREATE KEYSPACE IF NOT EXISTS operation_log
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
    """
)
sess.set_keyspace('operation_log')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
