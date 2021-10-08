from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for
from flask_login.utils import login_required
from werkzeug.utils import redirect
from a_cupcakes.forms import requestForm, BugReportForm
import smtplib, ssl
from a_cupcakes.models import Reviews, Announcement, Item, BugReports, db
from flask_login import current_user


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Announcement.query.paginate(page, 2, False)
    next_url = url_for('site.home', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('site.home', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', posts=posts.items, title='Home', 
                            next_url=next_url,prev_url=prev_url)

# Currently Not In Use (Future Update)
# @site.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html')

@site.route('/menu')
def menu():

    items = Item.query.all()

    return render_template('menu.html', items=items, title='Menu')

@site.route('/reviews')
def reviews():

    reviews = reversed(Reviews.query.all())

    return render_template('reviews.html', reviews=reviews, title='Review')

@site.route('/inquiries', methods = ['GET', 'POST'])
def inquiries():
    form = requestForm()

    # Autofill form with user account information
    if request.method == 'GET' and current_user.is_authenticated:
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email

    first_name = form.first_name.data
    last_name = form.last_name.data
    email = form.email.data
    date = form.date_needed.data
    description = form.description.data

    if first_name:
        port = 465 # For SSL
        sender_email = 'noreplycupcakes@gmail.com'
        receiver_email = 'marc31697@gmail.com'
        message = f"""Subject: New Request\n\nFrom: {first_name + ' ' + last_name}\nEmail: {email}\nDate Needed: {date}\nDescription: {description}"""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server:
            server.login(sender_email, '022420cup')
            server.sendmail(sender_email, receiver_email, message)
        
        flash('Your request has been sent in. Once it has been reviewed, you will receive an email with information about your order.', 'request-sent')

    return render_template('inquiry.html', form = form)

@site.route('/bugreport', methods=['GET', 'POST'])
def bugreport():
    form = BugReportForm()

    if request.method == 'GET' and not current_user.is_authenticated:
        flash('You must be signed in to submit a bug report', 'auth-failed')
        return redirect(url_for('auth.signin'))
    else:
        first_name = current_user.first_name
        last_name = current_user.last_name
        email = current_user.email


    if request.method == 'POST' and form.validate_on_submit():
        report = form.report.data

        bugreport = BugReports(first_name = first_name, last_name = last_name, email = email, report = report)
        db.session.add(bugreport)
        db.session.commit()

        flash(f'Your report has been submitted. Thanks for helping to make the site better!')
        return redirect(url_for('site.home'))
    

    return render_template('bugreport.html', form=form)

@site.route('/cart', methods=['GET', 'POST'])
def seecart():
    return render_template('cart.html')