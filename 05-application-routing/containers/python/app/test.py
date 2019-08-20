#!/usr/bin/env python3

import MySQLdb
from flask import Flask
app = Flask(__name__)

@app.route("/")
def databasetest():

    db = MySQLdb.connect(host="python-backend",
                        user="root", 
                        passwd="pass") 
    if db:
        db_output = "database connection works!"
    else:
        db_output = "db connection broke"

    return db_output

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)