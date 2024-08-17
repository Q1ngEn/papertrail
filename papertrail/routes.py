from flask import Flask, render_template, url_for, redirect, request, flash
from papertrail import app, db, bcrypt
from papertrail.models import Student, Subject, StudentSubject
from papertrail.forms import RegistrationForm, LoginForm, SubjectForm, DepositForm, ChargeForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def home():
    if current_user.is_authenticated:  # user is logged in
        balance = current_user.balance
    else:
        balance = 0
    return render_template('home.html', balance=balance)


@app.route('/subject', methods=["GET", "POST"])
@login_required  # user needs to be logged in
def subject():
    # check if subject is in database
    subject_test = Subject.query.first()
    if not subject_test:  # subjects are not in database
        subjects_data = [['h1bio', 'H1 Biology'], ['h1chem', 'H1 Chemistry'], ['h1cl', 'H1 Chinese'], ['h1econs', 'H1 Economics'],
            ['h1gp', 'H1 General Paper'], ['h1geo', 'H1 Geography'], ['h1hist', 'H1 History'], ['h1elit', 'H1 English Literature'],
            ['h1ml', 'H1 Malay'], ['h1math', 'H1 Math'], ['h1phy', 'H1 Physics'], ['h1tl', 'H1 Tamil'], ['h2art', 'H2 Art'],
            ['h2bio', 'H2 Biology'], ['h2chem', 'H2 Chemistry'], ['h2clit', 'H2 Chinese Literature'], ['h2comp', 'H2 Computing'],
            ['h2econs', 'H2 Economics'], ['h2fm', 'H2 Further Math'], ['h2geo', 'H2 Geography'], ['h2hist', 'H2 History'],
            ['h2elit', 'H2 English Literature'], ['h2mlit', 'H2 Malay Literature'], ['h2math', 'H2 Math'], ['h2phy', 'H2 Physics'], ['h2tlit', 'H2 Tamil Literature']]
        
        for subject in subjects_data:
            row = Subject(subj_abreviation=subject[0], subj_name=subject[1])
            db.session.add(row)
        db.session.commit()


    form = SubjectForm()
    if form.validate_on_submit():
        if form.validate_subject():
            # delete previous subject
            subjects_taken = current_user.subjects
            for subject in subjects_taken:
                db.session.delete(subject)

            # add gp
            gp = Subject.query.filter_by(subj_abreviation='h1gp').first()
            gp_subject = StudentSubject(stu_id=current_user.id, subj_id=gp.id)
            db.session.add(gp_subject)

            # check fo mtl
            if form.h1mtl.data != 'na':
                mtl = Subject.query.filter_by(subj_abreviation=form.h1mtl.data).first()
                student_mtl = StudentSubject(stu_id=current_user.id, subj_id=mtl.id)
                db.session.add(student_mtl)

            # add the rest of the subjects
            selected_options = [form.subject_1.data, form.subject_2.data, form.subject_3.data, form.subject_4.data]
            for option in selected_options:
                subject = Subject.query.filter_by(subj_abreviation=option).first()
                student_subject = StudentSubject(stu_id=current_user.id, subj_id=subject.id)
                db.session.add(student_subject)

            db.session.commit()  # commit changes

            flash("Subjects has been saved", "success")
            return redirect(url_for('home'))
        else:  # subjects are the same
            flash('Subjects must be different', 'danger')
             
    return render_template("subject.html", title="Subjects", form=form)


@app.route('/deposit', methods=['GET', 'POST'])
@login_required  # user needs to be logged in
def deposit():
    balance = current_user.balance

    form = DepositForm()
    if form.validate_on_submit():
        balance += form.amount.data

        # update database balance
        current_user.balance = balance
        db.session.commit()

        flash('Deposit successfully', 'success')
        return redirect(url_for('home'))

    return render_template('deposit.html', title='Deposit', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # user is logged in
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            # login user and apply remember me
            login_user(student, remember=form.remember.data)
            flash("Login successful", "success")
            return redirect(url_for('home'))
        else:
            # inform user that login is wrong
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template("login.html", title="Login", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # user is logged in
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.validate_cg(form.cg.data):
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            if form.role.data == 'lead':
                if form.leader_password.data == 'Papertrail_leader':
                    student = Student(name=form.username.data, cg=form.cg.data, role=form.role.data,
                                  email=form.email.data, password=hashed_password, balance=0)
                    db.session.add(student)  # add student to database
                    db.session.commit()

                    flash('Your account has been created! You are now able to log in', 'success')
                    return redirect(url_for('login'))
                else:
                    flash("Leader password is incorrect please check again", "danger")
                    
            else:  # role is a student
                student = Student(name=form.username.data, cg=form.cg.data, role=form.role.data,
                                  email=form.email.data, password=hashed_password, balance=0)
                db.session.add(student)  # add student to database
                db.session.commit()

                flash('Your account has been created! You are now able to log in', 'success')
                return redirect(url_for('login'))
            
    return render_template("register.html", title="Register", form=form)


@app.route('/charge', methods=['GET', 'POST'])
@login_required  # user needs to be logged in
def charge():
    student = Student.query.filter_by(current_user.id).first()
    balance = student.balance

    form = ChargeForm()
    if form.validate_on_submit():
        balance -= form.amount.data

        # update database balance
        student.balance = balance
        db.session.commit()

        flash("Transaction Completed", "success")
        return redirect(url_for("home"))
    return render_template('charge.html', title='Charge', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for('home'))
