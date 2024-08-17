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

     
     
