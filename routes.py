import os
import uuid
from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from sqlalchemy import func, or_
from app import app, db, login_manager
from models import Investor, Admin, Settings
from forms import InvestorRegistrationForm, AdminLoginForm, WhatsAppSettingsForm

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'jpg', 'jpeg', 'png'}

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InvestorRegistrationForm()
    
    if form.validate_on_submit():
        # Save uploaded file
        filename = None
        if form.identity_document.data:
            filename = save_uploaded_file(form.identity_document.data)
            if not filename:
                flash('Erreur lors du téléchargement du fichier. Veuillez réessayer.', 'danger')
                return render_template('index.html', form=form)
        
        # Create new investor
        investor = Investor(
            full_name=form.full_name.data,
            whatsapp_number=form.whatsapp_number.data,
            email=form.email.data,
            nationality=form.nationality.data,
            city_country=form.city_country.data,
            profession=form.profession.data,
            investment_amount=form.investment_amount.data,
            experience_level=form.experience_level.data,
            identity_document=filename,
            payment_method=form.payment_method.data,
            additional_remarks=form.additional_remarks.data,
            terms_accepted=form.terms_accepted.data
        )
        
        try:
            db.session.add(investor)
            db.session.commit()
            flash('Inscription réussie ! Redirection vers le groupe WhatsApp...', 'success')
            
            # Get WhatsApp group link
            settings = Settings.query.first()
            whatsapp_link = settings.whatsapp_group_link if settings else '#'
            
            return render_template('index.html', 
                                 form=InvestorRegistrationForm(),  # Reset form
                                 success=True,
                                 whatsapp_link=whatsapp_link)
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de l\'inscription. Veuillez réessayer.', 'danger')
            app.logger.error(f"Error saving investor: {e}")
    
    return render_template('index.html', form=form)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            flash('Connexion réussie !', 'success')
            return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
    
    return render_template('admin_login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Déconnexion réussie.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    experience_filter = request.args.get('experience', '')
    amount_filter = request.args.get('amount', '')
    
    # Build query
    query = Investor.query
    
    if search:
        query = query.filter(
            or_(
                Investor.full_name.contains(search),
                Investor.email.contains(search),
                Investor.whatsapp_number.contains(search)
            )
        )
    
    if experience_filter:
        query = query.filter(Investor.experience_level == experience_filter)
    
    if amount_filter:
        query = query.filter(Investor.investment_amount == amount_filter)
    
    # Pagination
    per_page = 50
    investors = query.order_by(Investor.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Statistics
    total_investors = Investor.query.count()
    
    # Calculate estimated total investment (simplified)
    investment_mapping = {
        '1000-5000': 3000,
        '5000-10000': 7500,
        '10000-25000': 17500,
        '25000-50000': 37500,
        '50000-100000': 75000,
        '100000+': 150000
    }
    
    total_estimated = 0
    for investor in Investor.query.all():
        total_estimated += investment_mapping.get(investor.investment_amount, 0)
    
    # Get WhatsApp settings
    settings = Settings.query.first()
    whatsapp_form = WhatsAppSettingsForm()
    if settings:
        whatsapp_form.whatsapp_group_link.data = settings.whatsapp_group_link
    
    return render_template('admin_dashboard.html', 
                         investors=investors,
                         total_investors=total_investors,
                         total_estimated=total_estimated,
                         search=search,
                         experience_filter=experience_filter,
                         amount_filter=amount_filter,
                         whatsapp_form=whatsapp_form,
                         settings=settings)

@app.route('/admin/update-whatsapp', methods=['POST'])
@login_required
def update_whatsapp():
    form = WhatsAppSettingsForm()
    
    if form.validate_on_submit():
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
        
        settings.whatsapp_group_link = form.whatsapp_group_link.data
        
        try:
            db.session.add(settings)
            db.session.commit()
            flash('Lien WhatsApp mis à jour avec succès !', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de la mise à jour.', 'danger')
            app.logger.error(f"Error updating WhatsApp link: {e}")
    else:
        flash('Données invalides.', 'danger')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/admin/export-csv')
@login_required
def export_csv():
    import csv
    from io import StringIO
    from flask import Response
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ID', 'Nom complet', 'WhatsApp', 'Email', 'Nationalité', 
        'Ville/Pays', 'Profession', 'Montant', 'Expérience', 
        'Paiement', 'Remarques', 'Date d\'inscription'
    ])
    
    # Write data
    for investor in Investor.query.all():
        writer.writerow([
            investor.id,
            investor.full_name,
            investor.whatsapp_number,
            investor.email,
            investor.nationality,
            investor.city_country,
            investor.profession,
            investor.investment_amount,
            investor.experience_level,
            investor.payment_method,
            investor.additional_remarks or '',
            investor.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=investisseurs.csv"}
    )

@app.errorhandler(413)
def too_large(e):
    flash('Le fichier est trop volumineux. Taille maximale autorisée : 16 MB', 'danger')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('base.html', error="Page non trouvée"), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('base.html', error="Erreur interne du serveur"), 500
