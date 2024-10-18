from flask import Blueprint, render_template, redirect, url_for
from .models import Client
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/clients')
@login_required
def clients():
    clients = Client.query.all()
    return render_template('client_list.html', clients=clients)
