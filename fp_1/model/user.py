from app2 import db
from model.login import LoginVO
from model.survey import surveyTable

class UserVO(db.Model):
    _tablename_ = 'user_table'
    user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    user_firstname = db.Column('user_firstname', db.String(100), nullable=False)
    user_lastname = db.Column('user_lastname', db.String(100), nullable=False)
    user_email_id = db.Column('user_emailid', db.String(100), nullable=False)
    user_contact = db.Column('user_contact', db.Numeric, nullable=False)
    user_login_id = db.Column('user_login_id', db.Integer, db.ForeignKey(LoginVO.login_id))
    # user_survey_id = db.Column('user_survey_id', db.Integer, db.ForeignKey(surveyTable.survey_id), nullable=True)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'user_firstname': self.user_firstname,
            'user_lastname': self.user_lastname,
            'user_email_id' : self.user_email_id,
            'user_contact': self.user_contact,
            'user_login_id': self.user_login_id,
            # 'user_survey_id': self.user_survey_id,
        }
db.create_all()