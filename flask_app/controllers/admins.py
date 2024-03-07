from flask_app import app
from flask import render_template, request, session, redirect, flash, url_for,sessions
from flask_bcrypt import Bcrypt
from flask_app.models.admin import Admin 
from flask_app.models.tour import Tour 


bcrypt = Bcrypt(app)

@app.route('/')
def home():
    tours=Tour.get_lowest_price()
    return render_template('index.html',tours=tours)

@app.route('/login')
def adminpage():
    if "user_id" in session:
        return redirect('/dashboard')
   
    return render_template('loginpage.html')



@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form["email"]}
    session['email']=request.form['email']
    user_in_db = Admin.get_admin_by_email(data)

    if not Admin.validate_user(request.form):
        return redirect(request.referrer)
    user = Admin.get_admin_by_email(request.form)
    if not user:
        flash('This email doesnt exist', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Incorrect password', 'passwordLogin')
        return redirect(request.referrer)
      

    if not user_in_db:
        flash("Invalid Email", 'loginemailerror')
        return redirect("/login")
  
    session['user_id'] = user_in_db['id']
    return redirect('/dashboard')

@app.route ('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    data={
        "id":session['user_id']
    
    }
    tours_nr=Tour.count_tours() #total number of tours
    payments_nr=Tour.count_payments() #total number of payments

    admin=Admin.get_admin_by_id(data)
    return render_template('sempleadmin.html', admin=admin , tours_nr= tours_nr, payments_nr=payments_nr)

#@app.route('/registerpg')
#def registerPage():
 #   return render_template('register.html')

