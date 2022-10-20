from finance_track import app, db
from finance_track.database_table import User, Role, SalesInvoice, Customer
from flask import render_template, request, session
from finance_track.database.run_system import *



@app.route('/')
def index():
    if 'role' in session:
        session.pop('role', None)
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    usercode = request.form['usercode']
    password = request.form['password']
    if usercode and password:
        system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
        response = system.log_in(usercode, password)
        if response == "sales admin":
            session['role'] = "sales admin"
            return "<script>window.location.href = '/admin_sale_page'; </script>"
        elif response == "finance":
            session['role'] = "finance"
            return "<script>window.location.href = '/finance_page'; </script>"
        elif response == "manager":
            session['role'] = "manager"
            return "<script>window.location.href = '/manager_page'; </script>"
        elif response == "wrong":
            return "<script>window.location.href = '/'; alert('Wrong Password'); </script>"
        elif response == "no user":
            return "<script>window.location.href = '/'; alert('No User'); </script>"
        else:
            return response
    return render_template('index.html')


@app.route('/admin_sale_page')
def admin_sales_page():
    if 'role' in session:
        if session['role'] == "sales admin":
            system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
            customers_list = system.list_all_customer()
            return render_template('admin_sale.html', data=customers_list)
        else:
            return "<script>window.location.href = '/'; </script>"
    else:
        return "<script>window.location.href = '/'; </script>"


@app.route('/sales_invoice')
def invoice_page():
    if 'role' in session:
        if session['role'] == "sales admin":
            system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
            sales_invoice_list = system.list_all_si()
            return render_template('sales_invoice.html', data=sales_invoice_list)
        else:
            return "<script>window.location.href = '/'; </script>"
    else:
        return "<script>window.location.href = '/'; </script>"


@app.route('/finance_page')
def finance_page():
    if 'role' in session:
        if session['role'] == "finance":
            system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
            sales_invoice_list = system.list_si_unpaid()
            return render_template('finance.html', si_=sales_invoice_list)
        else:
            return "<script>window.location.href = '/'; </script>"
    else:
        return "<script>window.location.href = '/'; </script>"


@app.route('/manager_page')
def manager_page():
    if 'role' in session:
        if session['role'] == "manager":
            system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
            total_fine = system.get_total_fine()
            si_unpaid_list = system.list_si_unpaid()
            return render_template('manager.html', data=total_fine, unpaid_list=si_unpaid_list)
        else:
            return "<script>window.location.href = '/'; </script>"
    else:
        return "<script>window.location.href = '/'; </script>"


@app.route('/customer_page')
def customer_page():
    if 'role' in session:
        if session['role'] == "manager":
            system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
            list_of_customers = system.list_customer()
            return render_template('customer.html', customers=list_of_customers)
        else:
            return "<script>window.location.href = '/'; </script>"
    else:
        return "<script>window.location.href = '/'; </script>"


@app.route('/user_page')
def user_page():
    if 'role' in session:
        if session['role'] == "manager":
            system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
            list_of_users = system.list_user()
            return render_template('user.html', list_of_users=list_of_users)
        else:
            return "<script>window.location.href = '/'; </script>"
    else:
        return "<script>window.location.href = '/'; </script>"


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
    if 'role' in session:
        if session['role'] == "manager":
            system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
            sales_invoice_list = system.list_all_si()
            return render_template('manager_sales_invoice.html', si=sales_invoice_list)
        else:
            return "<script>window.location.href = '/'; </script>"
    else:
        return "<script>window.location.href = '/'; </script>"


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


@app.route('/void', methods=['GET'])
def void():
    system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
    system.void_transaction(request.args.get('id_trans'))
    return "<script>alert('void'); window.location.href = '/manager_sales_invoice'; </script>"


@app.route('/get_customer', methods=['GET'])
def get_cust():
    system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
    customer = system.get_customer_info(request.args.get('cust_id'))
    return render_template('edit_customer.html', customer=customer)


@app.route('/edit_customer', methods=['POST', 'GET'])
def edit_customer():
    cust_id = request.form['cust_id']
    name = request.form['cust_name']
    address = request.form['address']
    tlp = request.form['tlp']
    status = request.form['status']
    system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
    response = system.edit_customer_data(cust_id, name, address, tlp, status)
    if response:
        return "<script>window.location.href = '/customer_page'; </script>"
    else:
        return "<script>alert('Fail to Edit'); window.location.href = '/customer_page'; </script>"

@app.route('/payment')
def payment():
    if 'role' in session:
        if session['role'] == "finance":
            si_id = request.args['si']
            si_id = si_id.split(',')
            system = DBSystem(db, User, Role, app, SalesInvoice, Customer)
            response = system.payment_sales_invoice(si_id)
            if response:
                return "<script>alert('Success Transaction'); window.location.href = '/finance_page'; </script>"
            else:
                return "<script>alert('Failed Transaction'); window.location.href = '/finance_page'; </script>"
        else:
            return "<script>window.location.href = '/'; </script>"
    else:
        return "<script>window.location.href = '/'; </script>"
