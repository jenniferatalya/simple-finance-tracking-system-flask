from finance_track import app, db
from finance_track.database_table import User, Role
from flask import render_template, request
from finance_track.database.run_system import *



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    usercode = request.form['usercode']
    password = request.form['password']

    if usercode and password:

        system = DBSystem(db, User, Role, app)
        response = system.log_in(usercode, password)

        if response == "sales admin":
            return render_template('admin_sale.html')
        elif response == "finance":
            return render_template('finance.html')
        elif response == "manager":
            return render_template('manager.html')
        elif response == "wrong":
            return "Wrong Password"
        elif response == "no user":
            return "No Username"
        else:
            return response
    return render_template('index.html')