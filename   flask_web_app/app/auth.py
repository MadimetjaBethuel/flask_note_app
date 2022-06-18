from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET','POST'])
def login():

    """
    authenticate user
    :params : noe
    :return: auth.html 
    """

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        # check user password
        if user:

            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success' ) # flash message on succcess
                login_user(user, remember=True)
                return redirect(url_for('views.home'))

            else:

                flash('Please check your password', category="error") # flash message on passoword failure
    
        else:
            flash("Email does not exist", category="error") # flash message on email failure 
    
    return render_template('login.html', user=current_user)


@auth.route('/logout')
def logout():
    """logs the user out """

    logout_user()

    return redirect(url_for('auth.login'))



@auth.route('/register', methods=['GET','POST'])
def register():

    """
    register new user
    :params : none
    : return : auth.html
    
    """

   
    if request.method == 'POST':

        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category="error")
        elif len(email) < 4 : # check the len of email
            flash('Email is too short', category="error")
    
        elif len(username) < 2 :
            flash('Username is too short', category="error")
        elif len(password) < 7:
            flash('Password is too short', category="error")
        elif password != confirm_password:
            flash('Passwords do not match', category="error")

        else:
            # create new user
            new_user = User(email=email,  firstname=username, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('You are now registered and can log in', category="success")
            return redirect(url_for('views.home'))

        
    return render_template('register.html', user=current_user)
            
               
                    