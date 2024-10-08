#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    #  a get method that gets all the plants in our database
    def get(self):
        #  creating a list that stores all the plants as a dictionary
        plants_list = [plant.to_dict() for plant in Plant.query.all()]
        #  creating and returning a response
        response = make_response(plants_list, 200)
        return response
    
    # a post method that creates a plant and posts it to the database
    def post(self):
        data = request.get_json()
        #  creating a new plant
        new_plant = Plant(
            name = data["name"],
            image = data["image"],
            price = data["price"]
        )

        # adding and commiting the new plant to the database
        db.session.add(new_plant)
        db.session.commit()

        #  creating a dictionary for the new plant using the to_dict()
        new_plant_dict = new_plant.to_dict()
        # creating and returning a response
        response = make_response(new_plant_dict, 200)
        return response
    pass


#  adding resource to the Plants class
api.add_resource(Plants, "/plants")

class PlantByID(Resource):
    #  a get method that gets a plant in our database by querying the id
    def get(self, id):
        # querying the plants table and getting the plant by the id
        plant = Plant.query.filter_by(id = id).first()
        #  displaying a plant as a dictionary
        plant_dict = plant.to_dict()
        # creating and returning a response
        response = make_response(plant_dict, 200)
        return response
    

    pass
#  adding resource to the PlantById class
api.add_resource(PlantByID, "/plants/<int:id>")

        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
