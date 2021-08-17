from flask import Flask, render_template, request, flash, redirect
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '46450e11e28426'
app.config['MAIL_PASSWORD'] = '72fb3830a310d4'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
app.config['SECRET_KEY'] = 'the random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
mail = Mail(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(1000))


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        email = request.form['email']
        name = request.form["name"]
        content = request.form["content"]
        message = Contact(name=name, email=email, content=content)
        msg = Message(subject='Hello From Derek', recipients=[email], body=content, sender='derekmiracledavid@gmail.com', attachments=None)
        mail.send(msg)
        db.session.add(message)
        db.session.commit()
        flash(f'Message sent to {email}')
        print(request.form['email'])
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)