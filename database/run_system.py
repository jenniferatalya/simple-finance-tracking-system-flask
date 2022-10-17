class DBSystem:
    def __init__(self, data_base, user_db, role_db, apps, si_db):
        self.db = data_base
        self.user_db = user_db
        self.role_db = role_db
        self.si_db = si_db
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

    def insert_sales_invoice(self, date_, user_id_, total_, remark_):
        with self.apps.app_context():
            try:
                si = self.si_db(date_, user_id_, total_, remark_, 'Unpaid', None)
                self.db.session.add(si)
                self.db.session.commit()
                return True
            except:
                return False

    def payment_sales_invoice(self, sales_invoices):
        sales_invoices_ = {}
        with self.apps.app_context():
            try:
                for i in range(len(sales_invoices)):
                    sales_invoices_[f'si{i}'] = self.si_db.query.where(self.si_db.id_trans==sales_invoices[i]).all()[0]
                for j in range(len(sales_invoices_)):
                    sales_invoices_[f'si{i}'].state = "Paid"
                    self.db.session.add(sales_invoices_[f'si{i}'])

                self.db.session.commit()
                return True
            except:
                return False