from flask_sqlalchemy import SQLAlchemy
from database.run_system import *
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='assets')

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root@127.0.0.1/tiny_jar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# class SalesInvoice(db.Model):
#     __tablename__ = 'Sales_Invoice'
#     id_trans = db.Column('id_trans', db.Integer, primary_key=True)
#     date = db.Column(db.DateTime)
#     cust_id = db.Column(db.Integer, db.ForeignKey("Customer.cust_id"))
#     total = db.Column(db.Integer)
#     remark = db.Column(db.Text)
#     state = db.Column(db.String(10))  # Unpaid, Paid, Void
#     paid_date = db.Column(db.DateTime)

#     def __init__(self, date, total, remark, state, paid_date):
#         self.date = date
#         self.total = total
#         self.remark = remark
#         self.state = state
#         self.paid_date = paid_date


# class Customer(db.Model):
#     __tablename__ = 'Customer'
#     cust_id = db.Column('cust_id', db.Integer, primary_key=True)
#     cust_name = db.Column(db.String(50))
#     cust_addr = db.Column(db.Text)
#     cust_tlp = db.Column(db.String(20))
#     cust_state = db.Column(db.String(10))  # Active, Not Active

#     def __init__(self, cust_name, cust_addr, cust_tlp, cust_state):
#         self.cust_name = cust_name
#         self.cust_addr = cust_addr
#         self.cust_tlp = cust_tlp
#         self.cust_state = cust_state


# class Role(db.Model):
#     __tablename__ = "Role"
#     role_id = db.Column('role_id', db.Integer, primary_key=True)
#     role_name = db.Column(db.String(15))  # Admin Sale, Finance, Manager
#     authority = db.Column(db.Text)

#     def __init__(self, role_name, authority):
#         self.role_name = role_name
#         self.authority = authority


# class User(db.Model):
#     __tablename__ = "User"
#     user_id = db.Column('user_id', db.Integer, primary_key=True)
#     user_name = db.Column(db.String(50))
#     user_pswd = db.Column(db.String(64))
#     role_id = db.Column(db.Integer, db.ForeignKey("Role.role_id"))

#     def __init__(self, user_name, user_pswd):
#         self.user_name = user_name
#         self.user_pswd = user_pswd


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    usercode = request.args.get['usercode']
    password = request.args.get['password']

    if usercode and password:
        
        system = DBSystem(db, User, Role, app)
        response = system.log_in(usercode, password)

        if response == "admin_sale":
            return render_template('admin_sale.html')
        elif response == "finance":
            return render_template('finance.html')
        elif response == "manager":
            return render_template('manager.html')
        elif response == "wrong":
            return 
        elif response == "no user":
            return
        else:
            return 0
    return render_template('index.html')