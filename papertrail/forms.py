from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from papertrail.models import Student

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    cg = StringField('Enter you CG (XX/XX)', validators=[DataRequired()])
    role = SelectField('Role', choices=[('stu', 'Student'), ('lead', 'Class Leader')], id='role')
    leader_password = PasswordField("Enter leader code")
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_cg(self, field):
        result = True
        if len(self.cg.data) != 5:
            result = False
            self.cg.errors.append("Invalid Length.")
        elif not self.cg.data[:2].isdigit():
            result = False
            self.cg.errors.append("Invalid format.")
        elif not self.cg.data[3:].isdigit():
            result = False
            self.cg.errors.append("Invalid format.")

        return result

    # check if username exists
    def validate_username(self, username):
        user = Student.query.filter_by(name=username.data).first()
        if user:
            raise ValidationError('That username is taken please choose anthor')
        
    # check if email already exists
    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken please choose another')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SubjectForm(FlaskForm):
    with app.app_context():
        subjects = Subject.query.all()
    subject_options = []
    
    # loop through every subject option
    for subject in subjects:
        # check if it is not mtl or gp
        if subject.subj_abreviation not in ['h1cl', 'h1ml', 'h1tl', 'h1gp']:
            subject_options.append((subject.subj_abreviation, subject.subj_name))
    
    subject_1 = SelectField(choices=subject_options)
    subject_2 = SelectField(choices=subject_options)
    subject_3 = SelectField(choices=subject_options)
    subject_4 = SelectField(choices=subject_options)
    h1mtl = SelectField("H1 Mother Tounge", choices=[('na', 'NA'), ('h1cl', 'H1 Chinese'), ('h1ml', 'H1 Malay'), ('h1tl', 'H1 Tamil')])

    def validate_subject(self):
        result = True
        seen = set()
        for field in [self.subject_1, self.subject_2, self.subject_3, self.subject_4]:
            if field.data in seen:
                field.errors.append('Please select distinct choices.')
                result = False
            else:
                seen.add(field.data)

        return result
    
    submit = SubmitField('Save changes')


class DepositForm(FlaskForm):
    amount = DecimalField('Amount Deposit:', validators=[DataRequired(), NumberRange(min=0, max=1000)])
    description = TextAreaField('Description')
    
    submit = SubmitField('Deposit')
    

class ChargeForm(FlaskForm):
    subjects = [('h2math', 'H2 Math'), ('h2phy', 'H2 Physics'), ('h2chem', 'H2 Chemistry'), ('h2bio', 'H2 Biology'),
                ('h2com', 'H2 Computing'), ('h2econ', 'H2 Economics'), ('h1econ', 'H1 Economics')]
    category = SelectField(choices=subjects)
    amount = DecimalField('Amount Deposit:', validators=[DataRequired(), NumberRange(min=0, max=50)])
    description = TextAreaField('Description')
    
    submit = SubmitField('Withdraw')
