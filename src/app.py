"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_people():
    search = People.query.all()    
    search_serialize = list(map(lambda x: x.serialize(), search)) # search.map((item)=>{item.serialize()})
    print("valor de search_serialize ", search_serialize)
    
    return jsonify(search_serialize), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_people_id(id):
    try:
        search = People.query.get(id)   
        search_serialize = search.serialize()
        print("valor de search_serialize ", search_serialize)    

        return jsonify(search_serialize), 200

    except Exception as error:
        print(error)
        return jsonify({"message":str(error)}), 500

@app.route('/people', methods=['POST'])
def add_people():
    try:
        body = request.get_json()
        
        new_register = People(
            name= body["name"],
            eye_color= body["eye_color"],
            hair_color= body["hair_color"],
            height= body["height"],
            age= body["age"]
        )

        db.session.add(new_register)
        db.session.commit()

        print("body es: ", body)

        return jsonify({"message":"El personaje se agregó"}), 200
    except Exception as error:
        print(error)
        return jsonify({"message":str(error)}), 500

@app.route('/people/<int:id>', methods=['PUT'])
def edit_people_id(id):
    try:
        body = request.get_json()
        search = People.query.get(id)   

        search.name = body["name"],
        search.eye_color = body["eye_color"],
        search.hair_color =  body["hair_color"],
        search.height =  body["height"],
        search.age = body["age"]
        db.session.commit()           

        return jsonify({"message":"se editó correctamente"}), 200

    except Exception as error:
        print(error)
        return jsonify({"message":str(error)}), 500

    
@app.route('/people/<int:id>', methods=['DELETE'])
def delete_people_id(id):
    try:
        
        search = People.query.get(id)   
        db.session.delete(search)
        db.session.commit()           

        return jsonify({"message":"se eliminó correctamente"}), 200

    except Exception as error:
        print(error)
        return jsonify({"message":str(error)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
