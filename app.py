import os
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

from forms import ContactoForm

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["MAIL_SERVER"] = "smtp.example.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_DEFAULT_SENDER"] = "proyecto@ejemplo.com"
app.config["MAIL_SUPPRESS_SEND"] = True

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
mail = Mail(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Usuario('{self.nombre}', '{self.correo}')"
 
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html", proyecto="Mi primera app con flask")

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    form = ContactoForm()
    if form.validate_on_submit():
        existence = Usuario.query.filter_by(correo=form.correo.data).first()
        if existence:
            flash("El correo ya esta en la base de datos", "danger")
        else:
            usuario = Usuario(nombre=form.nombre.data, correo=form.correo.data)
            db.session.add(usuario)
            db.session.commit()
            mensaje = Message(
                subject="Confirmacion de registro",
                recipients=[usuario.correo], 
                body=f"Hola {usuario.nombre}, Tu registro se guardo correctamente."
                )
            mail.send(mensaje)
            print(f"Correo de prueba para:", usuario.correo)
            flash(f'Registro guardado con exito, {usuario.nombre}', category="success")
            return redirect(url_for("contacto"))
    return render_template("contacto.html", form=form)

@app.route("/usuarios")
def usuarios():
    lista=Usuario.query.order_by(Usuario.id).all()
    return render_template("usuarios.html", usuarios=lista)

if __name__ == "__main__":
    app.run(debug=True)
