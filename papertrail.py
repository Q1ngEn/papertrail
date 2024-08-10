from flask import Flask, render_template, url_for, redirect, request, flash
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e52751703579269d27d78a5b0957e6a6'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/subject', methods=["GET", "POST"])
def subject():
    form = SubjectForm()
    if form.validate_on_submit():
        flash("Subjects has been saved", "success")
        return redirect(url_for('home'))
                        
    return render_template("subject.html", title="Subjects", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)

if __name__ == '__main__':
    app.run(debug=True)
