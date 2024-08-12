from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NoneOf, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SubjectForm(FlaskForm):
    subjects = [('h2math', 'H2 Math'), ('h2phy', 'H2 Physics'), ('h2chem', 'H2 Chemistry'), ('h2bio', 'H2 Biology'),
                ('h2com', 'H2 Computing'), ('h2econ', 'H2 Economics'), ('h1econ', 'H1 Economics')]
    
    subject_1 = SelectField(choices=subjects)
    subject_2 = SelectField(choices=subjects)
    subject_3 = SelectField(choices=subjects)
    subject_4 = SelectField(choices=subjects)

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
    
    submit = SubmitField('Make Deposit')
    

