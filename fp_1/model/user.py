from app import db
from model.login import loginTable


class Register(db.Model):
    _tablename_ = 'user_table'
    user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column('user_firstname', db.String(100), nullable=False)
    last_name = db.Column('user_lastname', db.String(100), nullable=False)
    email_id = db.Column('user_emailid', db.String(100), nullable=False)
    contact = db.Column('user_contact', db.Numeric, nullable=False)
    user_logged_id = db.Column('user_login_id', db.Integer, db.ForeignKey(loginTable.logged_id))
    # user_survey_id = db.Column('user_survey_id', db.Integer, db.ForeignKey(surveyTable.survey_id), nullable=True)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'user_firstname': self.first_name,
            'user_lastname': self.last_name,
            'user_email_id' : self.email_id,
            'user_contact': self.contact,
            'user_login_id': self.user_logged_id,
            # 'user_survey_id': self.user_survey_id,
        }
db.create_all()