from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from config import Config
from models import db, User, Client, Lead, Deal, Comment
from forms import ClientForm, LeadForm, DealForm, CommentForm
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Routes and Functions

@app.route('/')
def home():
    flash("Redirected to Home", "info")
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            session['user_id'] = user.id
            session['role'] = user.role
            flash("Logged in successfully", "success")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login to access the dashboard", "warning")
        return redirect(url_for('login'))
    if session['role'] == 'admin':
        return redirect(url_for('admin_panel'))
    flash("Welcome to your dashboard", "info")
    return render_template('dashboard.html')

# Admin Panel Route
@app.route('/admin')
def admin_panel():
    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('dashboard'))
    flash("Admin panel accessed", "info")
    return render_template('admin_panel.html')

# Client Routes
@app.route('/clients/new', methods=['GET', 'POST'])
def create_client():
    if 'user_id' not in session:
        flash("Please login to create a client", "warning")
        return redirect(url_for('login'))
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data
        )
        db.session.add(client)
        db.session.commit()
        flash("Client created successfully!", "success")
        return redirect(url_for('list_clients'))
    return render_template('create_client.html', form=form)

@app.route('/clients')
def list_clients():
    if 'user_id' not in session:
        flash("Please login to view clients", "warning")
        return redirect(url_for('login'))
    search_query = request.args.get('search', '')
    clients = Client.query.filter(Client.name.ilike(f"%{search_query}%")).all() if search_query else Client.query.all()
    flash(f"Loaded {len(clients)} clients", "info")
    return render_template('list_clients.html', clients=clients)

@app.route('/clients/<int:client_id>')
def view_client(client_id):
    if 'user_id' not in session:
        flash("Please login to view client details", "warning")
        return redirect(url_for('login'))
    client = Client.query.get_or_404(client_id)
    leads = Lead.query.filter_by(client_id=client_id).all()
    form = CommentForm()  # Añadido para agregar comentarios
    flash(f"Viewing client {client.name}", "info")
    return render_template('view_client.html', client=client, leads=leads, form=form)

@app.route('/clients/<int:client_id>/convert_to_lead')
def convert_client_to_lead(client_id):
    if 'user_id' not in session:
        flash("Please login to convert client to lead", "warning")
        return redirect(url_for('login'))
    client = Client.query.get_or_404(client_id)
    lead = Lead(
        name=client.name,
        client_id=client.id,
        status="new",
        phone=client.phone,
        email=client.email,
        address=client.address
    )
    db.session.add(lead)
    db.session.commit()
    flash("Client successfully converted to Lead!", "success")
    return redirect(url_for('list_leads'))

# Lead Routes
@app.route('/leads/new', methods=['GET', 'POST'])
def create_lead():
    if 'user_id' not in session:
        flash("Please login to create a lead", "warning")
        return redirect(url_for('login'))
    form = LeadForm()
    if form.validate_on_submit():
        lead = Lead(
            name=form.name.data,
            status=form.status.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data
        )
        db.session.add(lead)
        db.session.commit()
        flash("Lead created successfully!", "success")
        return redirect(url_for('list_leads'))
    return render_template('create_lead.html', form=form)

@app.route('/leads')
def list_leads():
    if 'user_id' not in session:
        flash("Please login to view leads", "warning")
        return redirect(url_for('login'))
    leads = Lead.query.all()
    flash(f"Loaded {len(leads)} leads", "info")
    return render_template('list_leads.html', leads=leads)

@app.route('/leads/<int:lead_id>')
def view_lead(lead_id):
    if 'user_id' not in session:
        flash("Please login to view lead details", "warning")
        return redirect(url_for('login'))
    lead = Lead.query.get_or_404(lead_id)
    flash(f"Viewing lead {lead.name}", "info")
    return render_template('view_lead.html', lead=lead)

@app.route('/leads/<int:lead_id>/edit', methods=['GET', 'POST'])
def edit_lead(lead_id):
    if 'user_id' not in session:
        flash("Please login to edit lead", "warning")
        return redirect(url_for('login'))
    lead = Lead.query.get_or_404(lead_id)
    form = LeadForm(obj=lead)

    if form.validate_on_submit():
        lead.name = form.name.data
        lead.status = form.status.data
        lead.phone = form.phone.data
        lead.email = form.email.data
        lead.address = form.address.data
        db.session.commit()
        flash("Lead updated successfully!", "success")
        return redirect(url_for('list_leads'))

    flash("Editing lead details", "info")
    return render_template('edit_lead.html', form=form, lead=lead)

@app.route('/leads/<int:lead_id>/delete', methods=['POST'])
def delete_lead(lead_id):
    if 'user_id' not in session:
        flash("Please login to delete lead", "warning")
        return redirect(url_for('login'))
    
    lead = Lead.query.get_or_404(lead_id)
    db.session.delete(lead)
    db.session.commit()
    flash("Lead deleted successfully!", "success")
    return redirect(url_for('list_leads'))

@app.route('/leads/<int:lead_id>/convert', methods=['GET', 'POST'])
def convert_lead_to_deal(lead_id):
    if 'user_id' not in session:
        flash("Please login to convert lead to deal", "warning")
        return redirect(url_for('login'))
    lead = Lead.query.get_or_404(lead_id)
    form = DealForm()

    if request.method == 'GET':
        form.policy_number.data = f"POL-{lead.id}-{datetime.now().year}"
        form.insurer.data = "Insurer Name"
        form.start_date.data = datetime.now().date()
        form.renewal_date.data = form.start_date.data + timedelta(days=365)
        form.comments.data = f"Converted from Lead: {lead.name}\n" 

    if form.validate_on_submit():
        deal = Deal(
            policy_number=form.policy_number.data,
            insurer=form.insurer.data,
            product_category=form.product_category.data,
            start_date=form.start_date.data,
            renewal_date=form.renewal_date.data,
            client_id=lead.client_id
        )
        db.session.add(deal)
        db.session.commit()
        flash("Lead successfully converted to Deal!", "success")
        return redirect(url_for('list_deals'))

    return render_template('create_deal.html', form=form)

@app.route('/deals/new', methods=['GET', 'POST'])
def create_deal():
    if 'user_id' not in session:
        flash("Please login to create a deal", "warning")
        return redirect(url_for('login'))
    form = DealForm()
    if form.validate_on_submit():
        deal = Deal(
            policy_number=form.policy_number.data,
            insurer=form.insurer.data,
            product_category=form.product_category.data,
            start_date=form.start_date.data,
            renewal_date=form.renewal_date.data
        )
        db.session.add(deal)
        db.session.commit()
        flash("Deal created successfully!", "success")
        return redirect(url_for('list_deals'))
    return render_template('create_deal.html', form=form)

@app.route('/deals')
def list_deals():
    if 'user_id' not in session:
        flash("Please login to view deals", "warning")
        return redirect(url_for('login'))
    deals = Deal.query.all()
    flash(f"Loaded {len(deals)} deals", "info")
    return render_template('list_deals.html', deals=deals)

# Edit Deal Route
@app.route('/deals/<int:deal_id>/edit', methods=['GET', 'POST'])
def edit_deal(deal_id):
    if 'user_id' not in session:
        flash("Please login to edit the deal", "warning")
        return redirect(url_for('login'))
    
    deal = Deal.query.get_or_404(deal_id)
    form = DealForm(obj=deal)

    if form.validate_on_submit():
        deal.policy_number = form.policy_number.data
        deal.insurer = form.insurer.data
        deal.product_category = form.product_category.data
        deal.start_date = form.start_date.data
        deal.renewal_date = form.renewal_date.data
        db.session.commit()
        flash("Deal updated successfully!", "success")
        return redirect(url_for('list_deals'))

    return render_template('edit_deal.html', form=form, deal=deal)

# Delete Deal Route
@app.route('/deals/<int:deal_id>/delete', methods=['POST'])
def delete_deal(deal_id):
    if 'user_id' not in session:
        flash("Please login to delete the deal", "warning")
        return redirect(url_for('login'))
    
    deal = Deal.query.get_or_404(deal_id)
    db.session.delete(deal)
    db.session.commit()
    flash("Deal deleted successfully!", "success")
    return redirect(url_for('list_deals'))

# Deal Details with Comments
@app.route('/deals/<int:deal_id>', methods=['GET', 'POST'])
def view_deal(deal_id):
    if 'user_id' not in session:
        flash("Please login to view deal details", "warning")
        return redirect(url_for('login'))
    deal = Deal.query.get_or_404(deal_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(content=form.content.data, deal_id=deal.id)
        db.session.add(comment)
        db.session.commit()
        flash("Comment added successfully!", "success")
        return redirect(url_for('view_deal', deal_id=deal.id))

    comments = Comment.query.filter_by(deal_id=deal.id).order_by(Comment.timestamp.desc()).all()
    flash(f"Loaded {len(comments)} comments for deal {deal.policy_number}", "info")
    return render_template('view_deal.html', deal=deal, form=form, comments=comments)

# Route to add comments to deals from the client view
@app.route('/deals/<int:deal_id>/add_comment', methods=['POST'])
def add_comment(deal_id):
    if 'user_id' not in session:
        flash("Please login to add a comment", "warning")
        return redirect(url_for('login'))
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, deal_id=deal_id)
        db.session.add(comment)
        db.session.commit()
        flash("Comment added successfully!", "success")
    return redirect(url_for('view_deal', deal_id=deal_id))

# Renewal Reminder Function
def send_renewal_reminder():
    today = datetime.now().date()
    reminder_date = today + timedelta(days=30)
    deals_due_for_renewal = Deal.query.filter(Deal.renewal_date == reminder_date).all()
    for deal in deals_due_for_renewal:
        client = Client.query.get(deal.client_id)
        msg = Message("Policy Renewal Reminder",
                      sender="insurance_reminder@example.com",
                      recipients=[client.email, "insurance_reminder@example.com"])
        msg.body = f"Dear {client.name}, policy #{deal.policy_number} is due for renewal soon."
        mail.send(msg)

if __name__ == "__main__":
    app.run(debug=True, port=7000)
