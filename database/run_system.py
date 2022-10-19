class SIDto:
    def __init__(self, no_trans, date_in, customer_id, total, remark, status, date_pay):
        self.no_trans = no_trans
        self.date_in = date_in
        self.customer_id = customer_id
        self.total = total
        self.remark = remark
        self.status = status
        self.date_pay = date_pay


class UserDto:
    def __init__(self, user_id, username, user_pswd, role_name):
        self.user_id = user_id
        self.username = username
        self.user_pswd = user_pswd
        self.role_name = role_name


class CustomerDto:
    def __init__(self, customer_code, customer_name, customer_addr, customer_tlp, customer_status, total_debt):
        self.customer_code = customer_code
        self.customer_name = customer_name
        self.customer_addr = customer_addr
        self.customer_tlp = customer_tlp
        self.customer_status = customer_status
        self.total_debt = total_debt

class CustomerInfoDto:
    def __init__(self, customer_code, customer_name, customer_addr, customer_tlp, customer_status):
        self.customer_code = customer_code
        self.customer_name = customer_name
        self.customer_addr = customer_addr
        self.customer_tlp = customer_tlp
        self.customer_status = customer_status


class DBSystem:
    def __init__(self, data_base, user_db, role_db, apps, si_db, cust_db):
        self.db = data_base
        self.user_db = user_db
        self.role_db = role_db
        self.si_db = si_db
        self.cust_db = cust_db
        self.apps = apps

    def create_db(self):
        with self.apps.app_context():
            self.db.create_all()

    def delete_db(self):
        with self.apps.app_context():
            self.db.drop_all()

    def log_in(self, username, password):
        with self.apps.app_context():
            user_ = self.user_db.query.where(self.user_db.user_id == username).all()
            if len(user_) != 0:
                user_id_ = user_[0]
                password_in = user_id_.user_pswd
                if password_in == password:
                    role_id_ = user_id_.role_id
                    role_ = self.role_db.query.where(self.role_db.role_id == role_id_).all()
                    return role_[0].role_name

                else:
                    return "wrong"
            else:
                return "no user"

    def list_all_customer(self):
        with self.apps.app_context():
            cust_ = self.cust_db.query.all()
            customers_ = []
            for i in range(len(cust_)):
                customers_.append((cust_[i].cust_id, cust_[i].cust_name))
            return customers_

    def insert_sales_invoice(self, date_, cust_id_, total_, remark_):
        with self.apps.app_context():
            cust_ = self.cust_db.query.where(self.cust_db.cust_id == cust_id_).all()
            if len(cust_) != 0:
                cust_id_s = cust_[0]
                if cust_id_s.cust_state == 'Active':
                    try:
                        si = self.si_db(date_, int(cust_id_), int(total_), remark_, 'Unpaid', None)
                        self.db.session.add(si)
                        self.db.session.commit()
                        return True
                    except:
                        return False
                else:
                    return f'{cust_id_}Not Active'

    def payment_sales_invoice(self, sales_invoices):
        sales_invoices_ = {}
        with self.apps.app_context():
            try:
                for i in range(len(sales_invoices)):
                    sales_invoices_[f'si{i}'] = self.si_db.query.where(self.si_db.id_trans == sales_invoices[i]).all()[
                        0]
                for j in range(len(sales_invoices_)):
                    sales_invoices_[f'si{i}'].state = "Paid"
                    self.db.session.add(sales_invoices_[f'si{i}'])

                self.db.session.commit()
                return True
            except:
                return False

    def list_all_si(self):
        with self.apps.app_context():
            si_ = self.si_db.query.all()
            invoices = []
            for i in range(len(si_)):
                invoices.append(
                    SIDto(
                        si_[i].id_trans,
                        si_[i].date,
                        si_[i].cust_id,
                        si_[i].total,
                        si_[i].remark,
                        si_[i].state,
                        si_[i].paid_date
                    )
                )
            return invoices

    def get_total_fine(self):
        with self.apps.app_context():
            si_ = self.si_db.query.where(self.si_db.state == 'Unpaid').all()
            total_fine = 0
            for i in range(len(si_)):
                total_fine += si_[i].total

            return total_fine

    def list_si_unpaid(self):
        with self.apps.app_context():
            si_ = self.si_db.query.where(self.si_db.state == 'Unpaid').order_by('date').all()
            invoices = []
            for i in range(len(si_)):
                invoices.append(
                    SIDto(
                        si_[i].id_trans,
                        si_[i].date,
                        si_[i].cust_id,
                        si_[i].total,
                        si_[i].remark,
                        si_[i].state,
                        si_[i].paid_date
                    )
                )
            return invoices

    def list_user(self):
        with self.apps.app_context():
            users_ = self.user_db.query.all()
            list_of_users = []
            for i in range(len(users_)):
                curr_role = self.role_db.query.where(self.role_db.role_id == users_[i].role_id).all()[0].role_name
                list_of_users.append(
                    UserDto(
                        users_[i].user_id,
                        users_[i].user_name,
                        users_[i].user_pswd,
                        curr_role
                    )
                )
            return list_of_users

    def create_user(self, name, password, role):
        with self.apps.app_context():
            try:
                user_ = self.user_db(name, password, role)
                self.db.session.add(user_)
                self.db.session.commit()
                return True
            except:
                return False

    def create_customer(self, name, address, phone):
        with self.apps.app_context():
            try:
                cust_ = self.cust_db(name, address, phone, 'Active')
                self.db.session.add(cust_)
                self.db.session.commit()
                return True
            except:
                return False

    def list_customer(self):
        with self.apps.app_context():
            customers_ = self.cust_db.query.all()
            list_of_customers = []
            for i in range(len(customers_)):
                curr_debt = self.si_db.query.where(self.si_db.cust_id == customers_[i].cust_id).all()
                curr_total = 0
                for j in range(len(curr_debt)):
                    curr_total += curr_debt[j].total
                list_of_customers.append(
                    CustomerDto(
                        customers_[i].cust_id,
                        customers_[i].cust_name,
                        customers_[i].cust_addr,
                        customers_[i].cust_tlp,
                        customers_[i].cust_state,
                        curr_total
                    )
                )
            return list_of_customers

    def void_transaction(self, id_):
        with self.apps.app_context():
            si_ = self.si_db.query.where(self.si_db.id_trans == id_).all()[0]
            si_.state = 'Void'
            self.db.session.add(si_)
            self.db.session.commit()

    def get_customer_info(self, id_):
        with self.apps.app_context():
            customer_ = self.cust_db.query.where(self.cust_db.cust_id == id_).all()[0]
            return CustomerInfoDto(
                customer_.cust_id,
                customer_.cust_name,
                customer_.cust_addr,
                customer_.cust_tlp,
                customer_.cust_state
            )
