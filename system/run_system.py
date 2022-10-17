from app import db, app


class DBSystem:
    def __init__(self, data_base):
        self.db = data_base

    def create_db(self):
        with app.app_context():
            self.db.create_all()


if __name__ == "__main__":
    dbsistem = DBSystem(db)
    dbsistem.create_db()
