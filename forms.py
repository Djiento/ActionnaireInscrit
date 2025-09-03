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
    
    nationality = SelectField('Nationalité', validators=[
        DataRequired(message='Veuillez sélectionner votre nationalité')
    ], choices=[
        ('', 'Sélectionnez votre nationalité'),
        ('algérienne', 'Algérienne'),
        ('béninoise', 'Béninoise'),
        ('burkinabé', 'Burkinabé'),
        ('camerounaise', 'Camerounaise'),
        ('centrafricaine', 'Centrafricaine'),
        ('comorienne', 'Comorienne'),
        ('congolaise_brazzaville', 'Congolaise (Brazzaville)'),
        ('congolaise_kinshasa', 'Congolaise (Kinshasa)'),
        ('djiboutienne', 'Djiboutienne'),
        ('égyptienne', 'Égyptienne'),
        ('française', 'Française'),
        ('gabonaise', 'Gabonaise'),
        ('ghanéenne', 'Ghanéenne'),
        ('guinéenne', 'Guinéenne'),
        ('ivoirienne', 'Ivoirienne'),
        ('malienne', 'Malienne'),
        ('marocaine', 'Marocaine'),
        ('mauritanienne', 'Mauritanienne'),
        ('nigériane', 'Nigériane'),
        ('nigérienne', 'Nigérienne'),
        ('sénégalaise', 'Sénégalaise'),
        ('tchadienne', 'Tchadienne'),
        ('togolaise', 'Togolaise'),
        ('tunisienne', 'Tunisienne'),
        ('autre', 'Autre')
    ])
    
    city_country = SelectField('Ville / Pays de résidence', validators=[
        DataRequired(message='Veuillez sélectionner votre ville/pays de résidence')
    ], choices=[
        ('', 'Sélectionnez votre ville/pays'),
        ('abidjan_cote_ivoire', 'Abidjan, Côte d\'Ivoire'),
        ('accra_ghana', 'Accra, Ghana'),
        ('bamako_mali', 'Bamako, Mali'),
        ('bangui_centrafrique', 'Bangui, République Centrafricaine'),
        ('brazzaville_congo', 'Brazzaville, Congo'),
        ('cotonou_benin', 'Cotonou, Bénin'),
        ('dakar_senegal', 'Dakar, Sénégal'),
        ('douala_cameroun', 'Douala, Cameroun'),
        ('kinshasa_rdc', 'Kinshasa, RD Congo'),
        ('libreville_gabon', 'Libreville, Gabon'),
        ('lome_togo', 'Lomé, Togo'),
        ('ndjamena_tchad', 'N\'Djamena, Tchad'),
        ('niamey_niger', 'Niamey, Niger'),
        ('nouakchott_mauritanie', 'Nouakchott, Mauritanie'),
        ('ouagadougou_burkina', 'Ouagadougou, Burkina Faso'),
        ('paris_france', 'Paris, France'),
        ('yaounde_cameroun', 'Yaoundé, Cameroun'),
        ('autre', 'Autre')
    ])
    
    profession = StringField('Profession / Activité principale', validators=[
        DataRequired(message='La profession est obligatoire'),
        Length(min=2, max=100, message='La profession doit contenir entre 2 et 100 caractères')
    ])
    
    investment_amount = SelectField('Montant estimé à investir', validators=[
        DataRequired(message='Veuillez sélectionner un montant')
    ], choices=[
        ('', 'Sélectionnez un montant'),
        ('100000', '100 000 FCFA'),
        ('200000', '200 000 FCFA'),
        ('300000', '300 000 FCFA'),
        ('400000', '400 000 FCFA'),
        ('500000', '500 000 FCFA'),
        ('5000000+', '5 000 000 FCFA et plus')
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
