from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SelectField, IntegerField, TextAreaField, BooleanField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email ID', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=8, message='Password must be exactly 8 characters long')])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('', 'Select'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=120, message='Age must be between 1 and 120')])
    mobile = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=10, message='Mobile number must be 10 digits')])
    email = StringField('Email ID', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, max=8, message='Password must be exactly 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')
    
    def validate_mobile(self, field):
        if not field.data.isdigit():
            raise ValidationError('Mobile number must contain only digits')

class UploadForm(FlaskForm):
    document = FileField('Choose Document', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'txt', 'docx'], 'Only PDF, TXT, and DOCX files are allowed!')
    ])
    submit = SubmitField('Upload')

class FeedbackForm(FlaskForm):
    satisfied = RadioField('Do you satisfy with our service?', 
                          choices=[('yes', 'Yes'), ('no', 'No')], 
                          default='yes',
                          validators=[DataRequired()])
    message = TextAreaField('Write your Suggestions:', validators=[DataRequired()])
    submit = SubmitField('Submit')
