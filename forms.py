from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterForm1(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )

class RegisterForm2(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    phone = TextField(
        'Phone', validators=[DataRequired(), Length(min=10, max=10)]
    )
    address = TextField(
        'Address', validators=[DataRequired(), Length(min=1, max=100)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    """confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )"""

class LoginForm(Form):
    phone = TextField('Phone', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
class LoginForm2(Form):
    phone=TextField('Phone',[DataRequired()])
    password=PasswordField('Password',[DataRequired()])

class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
