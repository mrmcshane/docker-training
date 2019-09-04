#!/usr/bin/env python3

import MySQLdb
import hvac
import os
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def databasetest():

    client = hvac.Client()
    client = hvac.Client(
        url=os.environ['VAULT_URL'],
        token=os.environ['VAULT_TOKEN']
    )
    vault_data = client.read('kv/data/orange-python').get("data").get("data")

    return render_template('index.html', vault_data=vault_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)