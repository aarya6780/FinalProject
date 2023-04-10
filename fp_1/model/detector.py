from app import db

class detectorTable(db.Model):
    _tablename_ = 'ai_detector'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    input = db.Column('input', db.String, nullable=False)
    value = db.Column('value', db.String, nullable=False)
    user_email = db.Column('email',db.String, nullable=False)
    def as_dict(self):
        return {
            'id': self.id,
            'input': self.input,
            'value': self.value,
            'email' : self.user_email,
        }
db.create_all()