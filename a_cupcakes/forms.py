from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, length

# Sign In Form
class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Sign In')

# Sign Up Form
class UserSignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Sign Up')

# Inquiry Form
class requestForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    date_needed = StringField('Date Needed', validators=[DataRequired()])
    description = TextAreaField('Description of Request', validators=[DataRequired()])
    submit_button= SubmitField('Send Request')

# Item Form
class ItemForm(FlaskForm):
    type = StringField('Type', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    submit_button=SubmitField()

# Review Form
class ReviewForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    submit_button=SubmitField()

# Announcements Posting Form
class PostForm(FlaskForm):
    post = TextAreaField('Post', validators=[DataRequired()])
    submit_button = SubmitField('Post')

# Forgot Password Form
class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit_button = SubmitField('Reset Password')

# Reset Password Form
class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit_button=SubmitField('Change Password')

# Bug Report Form
class BugReportForm(FlaskForm):
    report = TextAreaField('Bug Report', validators=[DataRequired()])
    submit_button = SubmitField('Send Report')