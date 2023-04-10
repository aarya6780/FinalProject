from app import db


class loginTable(db.Model):
    _tablename_ = 'login'
    logged_id = db.Column('logged_id', db.Integer, primary_key=True, autoincrement=True)
    logged_useremail = db.Column('logged_useremail', db.String(100), nullable=False)
    logged_password = db.Column('logged_password', db.String(100), nullable=False)
    logged_secret = db.Column('logged_secret', db.String(32), nullable=False)

    def as_dict(self):
        return {
            'logged_id': self.logged_id,
            'logged_useremail': self.logged_useremail,
            'logged_password': self.logged_password,
            'logged_secret': self.logged_secret
        }


db.create_all()