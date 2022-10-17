from app import db, app, User, Role


class DBSystem:
    def __init__(self, data_base):
        self.db = data_base

    def create_db(self):
        with app.app_context():
            self.db.create_all()

    def delete_db(self):
        with app.app_context():
            self.db.drop_all()

    def log_in(self, username, password):
        with app.app_context():
            user_ = User.query.where(User.user_id == username).all()
            if len(user_) != 0:
                user_id_ = user_[0]
                password_in = user_id_.user_pswd
                if password_in == password:
                    role_id_ = user_id_.role_id
                    role_ = Role.query.where(Role.role_id == role_id_).all()
                    return role_[0].role_name

                else:
                    return "wrong"
            else:
                return "no user"


if __name__ == "__main__":
    dbsistem = DBSystem(db)
    print(dbsistem.log_in('141', 'akuganteng'))
    # dbsistem.delete_db()
