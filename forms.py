from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class DelegateForm(Form):
    newdelegate = StringField('delegate', validators=[DataRequired()])

class SearchForm(Form):
	finddelegate = StringField('account', validators=[DataRequired()])