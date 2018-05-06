import json
from flask import Flask, request


app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
