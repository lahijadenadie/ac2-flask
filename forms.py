from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class ContactoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(message="Escribe tu nombre")])
    correo =StringField(
        "correo",
        validators=[
            DataRequired(message="Escribe tu correo"),
            Email(message="Introduce un correo válido, por ejemplo ana@correo.com")
        ]
    )
    enviar = SubmitField("Enviar")