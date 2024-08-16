from datetime import datetime
from papertrail import app, db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(stu_id):
    return Student.query.get(int(stu_id))


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    cg = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    subjects = db.relationship("StudentSubject", backref='student', lazy=True)

    def __repr__(self):
        return f"Student('{self.name}', '{self.email}', {self.cg})"


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subj_abreviation = db.Column(db.String, nullable=False)
    subj_name = db.Column(db.String, nullable=False)
    students = db.relationship("StudentSubject", backref="subject", lazy=True)

    def __repr__(self):
        return f"Subject('{self.subj_code}', '{self.subj_name}')"
    

class StudentSubject(db.Model):
    stu_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    subj_id = db.Column(db.Integer, db.ForeignKey('subject.id'), primary_key=True)
    __table_args__ = (db.PrimaryKeyConstraint('stu_id', 'subj_id'),)
    
    def __repr__(self):
        return f"StudentSubject('{self.stu_id}', '{self.subj_id}')"

     
# add subjects to database
subjects = [['h1bio', 'H1 Biology'], ['h1chem', 'H1 Chemistry'], ['h1cl', 'H1 Chinese'], ['h1econs', 'H1 Economics'],
            ['h1gp', 'H1 General Paper'], ['h1geo', 'H1 Geography'], ['h1hist', 'H1 History'], ['h1elit', 'H1 English Literature'],
            ['h1ml', 'H1 Malay'], ['h1math', 'H1 Math'], ['h1phy', 'H1 Physics'], ['h1tl', 'H1 Tamil'], ['h2art', 'H2 Art'],
            ['h2bio', 'H2 Biology'], ['h2chem', 'H2 Chemistry'], ['h2clit', 'H2 Chinese Literature'], ['h2comp', 'H2 Computing'],
            ['h2econs', 'H2 Economics'], ['h2fm', 'H2 Further Math'], ['h2geo', 'H2 Geography'], ['h2hist', 'H2 History'],
            ['h2elit', 'H2 English Literature'], ['h2mlit', 'H2 Malay Literature'], ['h2math', 'H2 Math'], ['h2phy', 'H2 Physics'], ['h2tlit', 'H2 Tamil Literature']]

# add and create database
with app.app_context():
    db.create_all()
    for subject in subjects:
        row = Subject(subj_abreviation=subject[0], subj_name=subject[1])
        db.session.add(row)
    db.session.commit()
     