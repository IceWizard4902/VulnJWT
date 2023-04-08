from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, make_response
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from passlib.hash import sha256_crypt
from functools import wraps 
from sqlalchemy.sql import func

# Import the vulnerable implementation
import jwk, jku, kid

app = Flask(__name__)

# Postgres configuration
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'postgresql://postgres:postgres@localhost:5432/myflaskapp'

db = SQLAlchemy(app)

# Create "schema" for the users table in the database
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100))
    register_date = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<User {self.usernmae}>'

# Create "schema" for the articles table in the database
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), server_default=func.now())

# Index
@app.route("/")
def index():
    return render_template("home.html")

# About
@app.route("/about")
def about():
    return render_template("about.html")

# Articles
@app.route("/articles")
def articles():
    return render_template("articles.html", articles = Articles.query.all())

# Single article
@app.route("/article/<string:id>/")
def article(id):
    article = Articles.query.filter_by(id = id).first()
    return render_template("article.html", article = article)

# Register Form class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data 
        email = form.email.data 
        username = form.username.data 
        password = sha256_crypt.encrypt(str(form.password.data))

        new_user = Users(name=name, email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form fields
        username = request.form['username']
        password_candidate = request.form['password']
        scenario = request.form['scenario']

        # Fetch password from database
        result = Users.query.filter_by(username = username).first()

        if result != None:
            password = result.password

            # Compare password (possibly vulnerable to timing attacks)
            if sha256_crypt.verify(password_candidate, password):
                # Correct credentials
                session['logged_in'] = True
                session['username'] = username 
                session['scenario'] = scenario

                response = make_response(redirect(url_for('dashboard')))
                
                if scenario == "JWK":
                    response.set_cookie('admin', jwk.generate_token(username))
                elif scenario == "JKU":
                    response.set_cookie('admin', jku.generate_token(username))
                else:
                    response.set_cookie('admin', kid.generate_token(username))
                
                flash("You are now logged in", 'success')

                return response
            else:
                # Error message is vulnerable to username enumeration
                error = 'Invalid login'
                return render_template('login.html', error=error)                
        else:
            # Error message is vulnerable to username enumeration
            error = 'Username not found'
            return render_template('login.html', error=error)
    
    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, please log in!", 'danger')
            return redirect(url_for('login'))

    return wrap

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Output the flag if the admin cookie is verified
    token = request.cookies.get('admin')
    if session['scenario'] == "JWK":
        session['admin'] = jwk.validate_token(token)
    elif session['scenario'] == "JKU":
        session['admin'] = jku.validate_token(token)
    else:
        session['admin'] = kid.validate_token(token)
    
    # Get articles 
    result = Articles.query.all()

    if result != None:
        return render_template('dashboard.html', articles = result) 
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)

# Article Form class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=255)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add Article
@app.route("/add_article", methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data 
        body = form.body.data 
        username = session['username']

        new_article = Articles(title = title, author = username, body = body)
        db.session.add(new_article)
        db.session.commit()

        flash('Article created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)

# Edit Article
@app.route("/edit_article/<string:id>", methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    # Get article by ID 
    article = Articles.query.get(id)

    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields 
    form.title.data = article.title
    form.body.data = article.body 

    if request.method == "POST" and form.validate():
        # Get title and body from form submitted
        title = request.form['title']
        body = request.form['body']

        # Update and then commit to database
        article.title = title 
        article.body = body 
        db.session.add(article)
        db.session.commit()

        flash('Article updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Article
@app.route("/delete_article/<string:id>", methods=['POST'])
@is_logged_in
def delete_article(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('admin')

    flash('You are now logged out', 'success')
    return response

# For JKU case, which needs a public key endpoint.
@app.route("/public_keys.json")
def pub_keys():
    return  """
            {
                "keys": [
                    {
                        "kty": "RSA",
                        "e": "AQAB",
                        "use": "sig",
                        "kid": "Nzv4oc46mMpaVnzKHKzTmh2Ajip_ITEGZLoGCbkZBIg",
                        "alg": "RS256",
                        "n": "sVnQN4Kf1UL52aQhfuEL30KxIawt4gFcbih1CQ3Xs3uY_RzRsZS8dkD-62P6rYRxNmHrlz7jt6G3ib7vl9Fit5CA4I70ekA8uBs9HFVwQGbSB5gT1bXDqSiy-9X6vLpsbQoaFD8ocGrrnoe71Eve_-hFGBPWmVR3lTGVYU9X1HWD0VuLdaRwMg5jXWfbNeai6EMhehp5oYzkbVKGyWffNy8lspKlk2TOSeS8t0pbLeDAlepj61kY9_3zZbVeobLGlPk25-0qIw8ytB_dZAM220CanMIQsXQds7Jixa7L924uEbssqZqFQF4FvQvFMT5Cv50KepZhMuPmZ8wX6Sdr-Q"
                    }
                ]
            }
            """
if __name__ == "__main__":
    # Secret key is some random string
    app.secret_key='!@iJkQD1..zDd$$#'
    app.run(debug=True, port=5000)