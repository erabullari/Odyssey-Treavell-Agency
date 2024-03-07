from flask import Flask ,flash,session
from flask_app.config.mysqlconnection import connectToMySQL

class Tour:
    db_name = 'agencytreavell'

    def __init__(self, data):
        # Initialize a Tour object with data
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.destination = data['destination']
        self.flight_time = data['flight_time']
        self.return_time = data['return_time']
        self.departure = data['departure']
        self.picture = data['picture']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        # Save tour data to the database
        query = "INSERT INTO tours (name, description, destination, flight_time, return_time, departure,picture,price) VALUES (%(name)s, %(description)s, %(destination)s, %(flight_time)s, %(return_time)s, %(departure)s,%(picture)s,%(price)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    
    @classmethod
    def updatepic(cls, data):
        query = "UPDATE users SET picture = %(image)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def get_all_tours(cls):
        query = "SELECT * FROM tours;"
        results = connectToMySQL(cls.db_name).query_db(query)
        tours = []
        for tour in results:
            tours.append(tour)
        return tours
    

    @classmethod  #total number of tours
    def count_tours(cls):
        query = "SELECT COUNT(*) AS total_tours FROM tours;"
        result = connectToMySQL(cls.db_name).query_db(query)
        if result:
                return result[0]['total_tours']
        else:
                return None
        
    @classmethod # 4 tours with lower price
    def get_lowest_price(cls):
        query = "SELECT * FROM tours ORDER BY price ASC LIMIT 4;"
        results = connectToMySQL(cls.db_name).query_db(query)
        tours = []
        for tour in results:
            tours.append(tour)
        return tours
    
    @classmethod # all tours with lower price
    def get_all_tours_lower_price(cls):
        query = "SELECT * FROM tours ORDER BY price ASC ;"
        results = connectToMySQL(cls.db_name).query_db(query)
        tours = []
        for tour in results:
            tours.append(tour)
        return tours
    
    @classmethod # all tours with hier price
    def get_all_tours_higest_price(cls):
        query = "SELECT * FROM tours ORDER BY price DESC ;"
        results = connectToMySQL(cls.db_name).query_db(query)
        tours = []
        for tour in results:
            tours.append(tour)
        return tours
    
    @classmethod
    def get_tour_by_id(cls, data):
        query = "SELECT * FROM tours WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        else:
            return None
        

    @classmethod
    def createPayment(cls, data):
        query = "INSERT INTO payments (firstName,lastName,email,personal_id,ammount,status,tour_id) VALUES (%(firstName)s,%(lastName)s,%(email)s,%(personal_id)s,%(ammount)s,%(status)s,%(tour_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all_payments(cls):
        query = "SELECT * FROM payments;"
        results = connectToMySQL(cls.db_name).query_db(query)
        payments = []
        for payment in results:
            payments.append(payment)
        return payments
    
    
    @classmethod
    def count_payments(cls):
        query = "SELECT COUNT(*) AS total_payments FROM payments;"
        result = connectToMySQL(cls.db_name).query_db(query)
        if result:
                return result[0]['total_payments']
        else:
                return None
        

    @classmethod
    def get_all_payments_with_tour(cls):
        query = "SELECT * FROM payments JOIN tours ON payments.tour_id = tours.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        payments = []
        for payment in results:
            payments.append(payment)
        return payments
    

    @classmethod
    def get_tour_by_id(cls, data):
        query = "SELECT * FROM tours WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        else:
            return False
        

    @classmethod
    def get_last_payment_id(cls,data):
        query = "SELECT id FROM payments WHERE tour_id = %(tour_id)s and personal_id = %(personal_id)s ORDER BY id DESC LIMIT 1;"
        result = connectToMySQL(cls.db_name).query_db(query, data)

        id = 0
        if result:
            id = result[0]['id']
        return id
   

    #get payment by id and joing left tours info
    @classmethod
    def get_payment_by_id(cls, data):
        query = "SELECT * FROM payments LEFT JOIN tours ON payments.tour_id = tours.id WHERE payments.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        else:
            return False