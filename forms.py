from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    address = StringField('Address')  # Field for address
    submit = SubmitField('Save Client')

class LeadForm(FlaskForm):
    name = StringField('Lead Name', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('appointment', 'Appointment'), 
        ('submitted', 'Submitted to Company'),
        ('proposal_sent', 'Proposal Sent'),
        ('accepted', 'Proposal Accepted'),
        ('closed', 'Closed Sale')
    ])
    phone = StringField('Phone')       # Field for phone
    email = StringField('Email', validators=[Email()])  # Field for email
    address = StringField('Address')   # Field for address
    submit = SubmitField('Save Lead')

class DealForm(FlaskForm):
    policy_number = StringField('Policy Number', validators=[DataRequired()])
    insurer = StringField('Insurer', validators=[DataRequired()])  # Field for insurance provider
    product_category = SelectField('Product Category', choices=[
        ('life_insurance', 'Life Insurance'),
        ('annuity', 'Annuity'),
        ('commercial_property', 'Commercial Property'),
        ('commercial_auto', 'Commercial Auto'),
        ('commercial_package', 'Commercial Package'),
        ('personal_package', 'Personal Package'),
        ('personal_auto', 'Personal Auto'),
        ('personal_property', 'Personal Property'),
        ('health_insurance', 'Health Insurance'),
        ('group_health_insurance', 'Group Health Insurance')
    ], validators=[DataRequired()])  # Dropdown for product category
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    renewal_date = DateField('Renewal Date', format='%Y-%m-%d', validators=[DataRequired()])
    comments = TextAreaField('Comments')  # Field for initial comments
    submit = SubmitField('Create Deal')

class CommentForm(FlaskForm):
    content = TextAreaField('Add Comment', validators=[DataRequired()])  # Comment content field
    submit = SubmitField('Add Comment')
