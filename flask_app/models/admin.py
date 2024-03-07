from flask import Flask ,flash,session
from flask_app.config.mysqlconnection import connectToMySQL
import re	   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Admin:
    db_name='agencytreavell'

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        
    
    @classmethod
    def save(cls,data):
        query="INSERT INTO admins (first_name,last_name ,email,password) VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

  
 
   
    
    @classmethod
    def get_admin_by_email(cls, data):
        query = 'SELECT * FROM admins where email = %(email)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
        
    @classmethod
    def get_admin_by_id(cls, data):
        query = 'SELECT * FROM admins where id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False


    @staticmethod
    def validate_user(user):
        is_valid=True
       
        if len(user['password'])<7:
            flash('Enter 8 character for pasword' , 'password')
            is_valid=False

        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!" ,'emailerror')
            is_valid = False
        return is_valid



    
    