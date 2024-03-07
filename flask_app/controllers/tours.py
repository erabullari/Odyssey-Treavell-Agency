from flask_app import app
from flask import flash, request, redirect,session ,render_template,request,url_for
from flask_app.models.tour import Tour
from flask_app.models.admin import Admin
from reportlab.pdfgen import canvas


import paypalrestsdk


import os   
from datetime import datetime
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from .env import ADMINEMAIL
from .env import PASSWORD





UPLOAD_FOLDER = 'flask_app/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/register/tour', methods=['POST'])
def register_tour():
    data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'destination': request.form['destination'],
            'flight_time': request.form['flight_time'],
            'return_time': request.form['return_time'],
            'departure': request.form['departure'],
            'price': request.form['price'] 
        }
    
    if 'picture' in request.files:
        picture = request.files['picture']
        if picture.filename != '':
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = secure_filename(picture.filename)
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], current_time + filename))
            data["picture"] = current_time + filename

    
    Tour.save(data)

    return redirect(request.referrer)  # Redirekto në faqen e hyrjes

@app.route("/add/photo", methods=["POST"])
def add_photo():
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "id": session['user_id']
    }
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], current_time + filename))
            data["image"] = current_time + filename
        
    Tour.add_profil_pic(data)
    return redirect(request.referrer)


@app.route('/add/tour')
def add_tour():
    if "user_id" not in session:
        return redirect("/login")    
    data={
        "id":session['user_id']
    }
    admin=Admin.get_admin_by_id(data)
    
    tours=Tour.get_all_tours()
    tours_nr=Tour.count_tours() #total number of tours
    payments_nr=Tour.count_payments() #total number of payments
    return render_template('add-new-tour.html',tours=tours ,admin=admin ,tours_nr=tours_nr, payments_nr=payments_nr)





@app.route('/tour/all')
def all_tours():
    if "user_id" not in session:
        return redirect("/login")
    data={
        "id":session['user_id']
    }
    admin=Admin.get_admin_by_id(data)

    tours=Tour.get_all_tours()
    tours_nr=Tour.count_tours() #total number of tours
    payments_nr=Tour.count_payments() #total number of payments

    return render_template('all-tours.html',tours=tours ,admin=admin ,tours_nr=tours_nr,payments_nr=payments_nr)


@app.route('/payments')
def all_payments():
    if "user_id" not in session:
        return redirect("/login")
    data={
        "id":session['user_id']
    }
    admin=Admin.get_admin_by_id(data)

    tours=Tour.get_all_tours()
    tours_nr=Tour.count_tours() #total number of tours
    payments_nr=Tour.count_payments() #total number of payments

    payments=Tour.get_all_payments_with_tour()
    return render_template('all-payments.html',tours=tours ,admin=admin ,tours_nr=tours_nr,payments_nr=payments_nr,payments=payments)



@app.route('/tours')
def tours():
    tours=Tour.get_all_tours()
    return render_template('tours.html',tours=tours)


@app.route('/tours/lower')
def tours_lower():
    tours=Tour.get_all_tours_lower_price()
    return render_template('tours-lower-price.html',tours=tours)


@app.route('/tours/higest')
def tours_higest():
    tours=Tour.get_all_tours_higest_price()
    return render_template('tours-higest-price.html',tours=tours)


@app.route('/bye/tour/<int:id>')
def bye_tour(id):
    tour =Tour.get_tour_by_id({'id': id})
    return render_template('bye-tour.html',tour=tour)


#app.route('/buy/tour', methods=['POST'])
#def buy_tour():
 #   data={
  #    'firstName':request.form['firstName'],
   #   'lastName':request.form['lastName'],
    #  'email':request.form['email'],
     # 'personal_id':request.form['personal_id'],
   #  }
   


    Client.save_client(data)
    return redirect(request.referrer)

@app.route('/about/tour')
def about_tour():
    return render_template('about.html')





@app.route('/checkout/paypal/<int:package_id>', methods=['POST'])
def checkoutPaypal(package_id):
    
    package = Tour.get_tour_by_id({'id': package_id})
    totalPrice = package['price']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    personal_id = request.form['personal_id']


    try:
        paypalrestsdk.configure({
            "mode": "sandbox", # Change this to "live" when you're ready to go live
            "client_id": "AY7gBFieOCMVALjMki-cmRPjiF3IJK8vxU55hqYIaXKZgg0iSmGjczyWYhUWxhdfFJzEvI3P9SyLKVBu",
            "client_secret": "EPAvLQmZFB5RroxrYb7chGMDqq6OnQ6hlxYH5DBKV_vkmqnezg-R_J9nGKbmGtfwoGYjXsW4EZbdG1IB"
        })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": totalPrice,
                    "currency": "USD"  # Adjust based on your currency
                },
                "description": f"Pagese per parkim per makinen me targe orë!"
            }],
            "redirect_urls": {
                "return_url": url_for('paymentSuccess', _external=True, totalPrice=totalPrice, firstName=firstName, lastName=lastName, email=email, personal_id=personal_id, package_id=package_id),
                "cancel_url": "http://example.com/cancel"
            }
        })

        if payment.create():
            approval_url = next(link.href for link in payment.links if link.rel == 'approval_url')
            return redirect(approval_url)
        else:
            flash('Something went wrong with your payment', 'creditCardDetails')
            return redirect(request.referrer)
    except paypalrestsdk.ResourceNotFound as e:
        flash('Something went wrong with your payment', 'creditCardDetails')
        return redirect(request.referrer)






@app.route("/success", methods=["GET"])
def paymentSuccess():
    payment_id = request.args.get('paymentId', '')
    payer_id = request.args.get('PayerID', '')
    try:
        paypalrestsdk.configure({
            "mode": "sandbox", # Change this to "live" when you're ready to go live
            "client_id": "AY7gBFieOCMVALjMki-cmRPjiF3IJK8vxU55hqYIaXKZgg0iSmGjczyWYhUWxhdfFJzEvI3P9SyLKVBu",
            "client_secret": "EPAvLQmZFB5RroxrYb7chGMDqq6OnQ6hlxYH5DBKV_vkmqnezg-R_J9nGKbmGtfwoGYjXsW4EZbdG1IB"
        })
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            
            print("////////////////////////////////////////////////////")
            
            ammount = request.args.get('totalPrice')
            status = 'Paid'
            package_id = request.args.get('package_id')
            data = {
                'ammount': ammount,
                'status': status,
                'firstName': request.args.get('firstName'),
                'lastName': request.args.get('lastName'),
                'email': request.args.get('email'),
                'personal_id': request.args.get('personal_id'),
                'tour_id': package_id
            }
            Tour.createPayment(data)

            payment_id = Tour.get_last_payment_id(data)
            flash('Your payment was successful!', 'paymentSuccessful')
            return redirect(url_for('pdf', payment_id=payment_id ))
        else:
            print("")
            flash('Something went wrong with your payment', 'paymentNotSuccessful')
            return redirect('/')
    except paypalrestsdk.ResourceNotFound as e:
        flash('Something went wrong with your payment', 'paymentNotSuccessful')
        return redirect('/')


@app.route("/cancel", methods=["GET"])
def paymentCancel():
    flash('Payment was canceled', 'paymentCanceled')
    return redirect('/')





#PDF
@app.route('/pdf')
def pdf():
    #get time as sting
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    #create pdf
    pdf_name = current_time + "payment.pdf"
    c = canvas.Canvas("flask_app/static/pdf/"+pdf_name)
    payment_id = request.args.get('payment_id')
    payment = Tour.get_payment_by_id({'id': payment_id})



    c.setFont("Helvetica", 12)
    c.drawString(100, 730, "First Name: " + payment['firstName'])
    c.drawString(100, 710, "Last Name: " + payment['lastName'])
    c.drawString(100, 690, "Email: " + payment['email'])
    c.drawString(100, 670, "Personal ID: " + payment['personal_id'])
    c.drawString(100, 650, "Amount: " + str(payment['ammount']))
    c.drawString(100, 630, "Status: " + payment['status'])
    c.drawString(100, 610, "Tour Name: " + payment['name'])
    c.drawString(100, 590, "Tour Description: " + payment['description'])
    c.drawString(100, 570, "Tour Destination: " + payment['destination'])
    c.drawString(100, 550, "Flight Time: " + payment['flight_time'])
    c.drawString(100, 530, "Return Time: " + payment['return_time'])
    c.drawString(100, 510, "Departure: " + payment['departure'])

    c.save()


    email_send = payment['email']
    #send email
    LOGIN = ADMINEMAIL
    TOADDRS  = email_send
    SENDER = ADMINEMAIL

    msg = MIMEMultipart()
    msg['From'] = LOGIN
    msg['To'] = email_send
    msg['Subject'] = 'Fatura jote'

    # Add body to the email
    body = 'Faleminderit qe zgjodhet sherbimin tone!'
    msg.attach(MIMEText(body, 'plain'))


    # Attach PDF file
    filename = pdf_name
    attachment = open("flask_app/static/pdf/"+pdf_name, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())



    # Encode the file and add headers
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)



    # Add attachment to message and convert message to string
    msg.attach(part)
    text = msg.as_string()

    # Log in to server using secure context and send email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(SENDER, TOADDRS, text)
    server.quit()

    
    return redirect('/')

