from finance_track import app, db
from finance_track.database_table import User, Role, SalesInvoice, Customer
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
        system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
        response = system.log_in(usercode, password)
        if response == "sales admin":
            return "<script>window.location.href = '/admin_sale_page'; </script>"
        elif response == "finance":
            return "<script>window.location.href = '/finance_page'; </script>"
        elif response == "manager":
            return "<script>window.location.href = '/manager_page'; </script>"
        elif response == "wrong":
            return "Wrong Password"
        elif response == "no user":
            return "No Username"
        else:
            return response
    return render_template('index.html')


@app.route('/admin_sale_page')
def admin_sales_page():
    system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
    customers_list = system.list_all_customer()
    return render_template('admin_sale.html', data=customers_list)


@app.route('/sales_invoice')
def invoice_page():
    system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
    sales_invoice_list = system.list_all_si()
    return render_template('sales_invoice.html', data=sales_invoice_list)


@app.route('/finance_page')
def finance_page():
    return render_template('finance.html')


@app.route('/manager_page')
def manager_page():
    system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
    total_fine = system.get_total_fine()
    si_unpaid_list = system.list_si_unpaid()
    return render_template('manager.html', data=total_fine, unpaid_list=si_unpaid_list)

@app.route('/customer_page')
def customer_page():
    system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
    list_of_customers = system.list_customer()
    return render_template('customer.html', customers=list_of_customers)

@app.route('/user_page')
def user_page():
    system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
    list_of_users = system.list_user()
    return render_template('user.html', list_of_users=list_of_users)

@app.route('/admin_sale', methods=['POST'])
def create_invoice():
    inv_date = request.form['inv_date']
    cust_id = request.form['cust_id']
    inv_total = request.form['inv_total']
    remark = request.form['inv_remark']

    if inv_date and cust_id and inv_total and remark:

        system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
        response = system.insert_sales_invoice(inv_date, cust_id, inv_total, remark)

        if response:
            return "<script>alert('Sales Invoice is Successfully Added'); window.location.href = '/admin_sale_page'; </script>"
        else:
            return "<script>alert('Failed'); window.location.href = '/admin_sale_page'; </script>"

@app.route('/new_user', methods=['POST'])
def add_new_user():
    name = request.form['user_name']
    password = request.form['password']
    role = request.form['role']
    
    if name and password and role:
        system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
        response = system.create_user(name, password, role)
        if response:
            return "<script>alert('New User is Successfully Added'); window.location.href = '/user_page'; </script>"
        else:
            return "<script>alert('Failed'); window.location.href = '/user_page'; </script>"

@app.route('/manager_sales_invoice')
def manager_si_page():
    system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
    sales_invoice_list = system.list_all_si()
    return render_template('manager_sales_invoice.html', si=sales_invoice_list)

@app.route('/new_customer', methods=['POST'])
def add_new_cust():
    name = request.form['cust_name']
    address = request.form['address']
    phone = request.form['tlp']
    
    if name and address and phone:
        system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
        response = system.create_customer(name, address, phone)
        if response:
            return "<script>alert('New Customer is Successfully Added'); window.location.href = '/customer_page'; </script>"
        else:
            return "<script>alert('Failed'); window.location.href = '/customer_page'; </script>"