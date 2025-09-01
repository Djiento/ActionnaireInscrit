from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, EmailField, TextAreaField, SelectField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import re

class InvestorRegistrationForm(FlaskForm):
    full_name = StringField('Nom complet', validators=[
        DataRequired(message='Le nom complet est obligatoire'),
        Length(min=2, max=100, message='Le nom doit contenir entre 2 et 100 caractères')
    ])
    
    whatsapp_number = StringField('Numéro WhatsApp', validators=[
        DataRequired(message='Le numéro WhatsApp est obligatoire'),
        Length(min=8, max=20, message='Le numéro doit contenir entre 8 et 20 caractères')
    ])
    
    email = EmailField('Adresse e-mail', validators=[
        DataRequired(message='L\'adresse e-mail est obligatoire'),
        Email(message='Veuillez entrer une adresse e-mail valide')
    ])
    
    nationality = StringField('Nationalité', validators=[
        DataRequired(message='La nationalité est obligatoire'),
        Length(min=2, max=50, message='La nationalité doit contenir entre 2 et 50 caractères')
    ])
    
    city_country = StringField('Ville / Pays de résidence', validators=[
        DataRequired(message='La ville/pays de résidence est obligatoire'),
        Length(min=2, max=100, message='La ville/pays doit contenir entre 2 et 100 caractères')
    ])
    
    profession = StringField('Profession / Activité principale', validators=[
        DataRequired(message='La profession est obligatoire'),
        Length(min=2, max=100, message='La profession doit contenir entre 2 et 100 caractères')
    ])
    
    investment_amount = SelectField('Montant estimé à investir', validators=[
        DataRequired(message='Veuillez sélectionner un montant')
    ], choices=[
        ('', 'Sélectionnez un montant'),
        ('1000-5000', '1 000 - 5 000 €'),
        ('5000-10000', '5 000 - 10 000 €'),
        ('10000-25000', '10 000 - 25 000 €'),
        ('25000-50000', '25 000 - 50 000 €'),
        ('50000-100000', '50 000 - 100 000 €'),
        ('100000+', '100 000 € et plus')
    ])
    
    experience_level = SelectField('Expérience en investissement', validators=[
        DataRequired(message='Veuillez sélectionner votre niveau d\'expérience')
    ], choices=[
        ('', 'Sélectionnez votre niveau'),
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé')
    ])
    
    identity_document = FileField('Pièce d\'identité', validators=[
        FileRequired(message='La pièce d\'identité est obligatoire'),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Seuls les fichiers PDF, JPG, JPEG et PNG sont autorisés')
    ])
    
    payment_method = SelectField('Moyen de paiement préféré', validators=[
        DataRequired(message='Veuillez sélectionner un moyen de paiement')
    ], choices=[
        ('', 'Sélectionnez un moyen de paiement'),
        ('mobile_money', 'Mobile Money'),
        ('virement', 'Virement bancaire'),
        ('autre', 'Autre')
    ])
    
    additional_remarks = TextAreaField('Remarques supplémentaires')
    
    terms_accepted = BooleanField('J\'accepte les conditions et la politique de confidentialité', validators=[
        DataRequired(message='Vous devez accepter les conditions et la politique de confidentialité')
    ])
    
    submit = SubmitField('S\'inscrire')

    def validate_whatsapp_number(self, field):
        # Remove spaces and common separators
        number = re.sub(r'[\s\-\(\)\+]', '', field.data)
        if not number.isdigit():
            raise ValidationError('Le numéro WhatsApp ne doit contenir que des chiffres')

class AdminLoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[
        DataRequired(message='Le nom d\'utilisateur est obligatoire')
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message='Le mot de passe est obligatoire')
    ])
    submit = SubmitField('Se connecter')

class WhatsAppSettingsForm(FlaskForm):
    whatsapp_group_link = StringField('Lien du groupe WhatsApp', validators=[
        DataRequired(message='Le lien du groupe WhatsApp est obligatoire'),
        Length(min=10, max=500, message='Le lien doit contenir entre 10 et 500 caractères')
    ])
    submit = SubmitField('Mettre à jour')
