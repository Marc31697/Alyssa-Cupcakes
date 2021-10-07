# from a_cupcakes import app, mail
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from a_cupcakes.forms import UserLoginForm, UserSignupForm, ForgotForm, PasswordResetForm
from a_cupcakes.models import User, db
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Mail, Message
from flask import url_for

auth = Blueprint('auth', __name__, template_folder='auth_templates')
mail = Mail()

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data

            user = User(first_name = first_name, last_name = last_name, email = email, password = password)
            db.session.add(user)
            db.session.commit()
            
            logged_user = User.query.filter(User.email == email).first()
            if logged_user:
                login_user(logged_user)
            flash(f'You have successfully created a user account {email}', 'user-created')

            return redirect(url_for('site.home'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    
    return render_template('signup.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in', 'auth-success')

                if current_user.admin == True:
                    return redirect(url_for('admin.admin_dashboard'))

                return redirect(url_for('site.home'))
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    
    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))

def send_password_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='noreplycupcakes@acupcakes.com')
    msg.body = f''' To reset your pasword. Please follow the link below.
    
    { url_for('auth.reset_token', token=token, _external=True) }

    If you did not send a password reset request, please ignore this message.
    
    '''
    print(msg)
    mail.send(msg)

@auth.route('/forgot', methods=('GET', 'POST'))
def forgot_password():
    form = ForgotForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_mail(user)
            flash('You will receive a password reset email if we find that email in our system', 'auth-failed')
            return redirect(url_for('auth.signin'))

        
        return redirect(url_for('signin.html'))
    return render_template('forgot.html', form = form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_token(token)
    if user is None:
        flash('Token expired. Please try again.','warning')
        return redirect(url_for('forgot_password'))
    
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Password Successfully Changed. Please log in!', 'success')
        return redirect(url_for('auth.signin'))
    
    return render_template('change_password.html', title = "Change Password", form = form)