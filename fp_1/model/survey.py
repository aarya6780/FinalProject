from app2 import db
from model.login import LoginVO

class surveyTable(db.Model):
    _tablename_ = 'survey_form_data'
    survey_id = db.Column('survey_id', db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column('firstname', db.String(100), nullable=False)
    lastname = db.Column('lastname', db.String(100), nullable=False)
    ratings = db.Column('ratings', db.Numeric, nullable=False)
    
    is_recommendable = db.Column('is_recommendable', db.String(100), nullable=False)
    feedbacks = db.Column('feedbacks', db.String(5000))

    def as_dict(self):
        return {
            'survey_id': self.survey_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'ratings' : self.ratings,
            'is_recommendable': self.is_recommendable,
            'feedbacks': self.feedbacks,
        }
db.create_all()