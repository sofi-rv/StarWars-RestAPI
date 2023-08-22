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
from models import db, User, People, FavoritePeople
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
    

@app.route('/favorite-people', methods=['GET'])
def get_favorite_people():
    search = FavoritePeople.query.all()    
    search_serialize = list(map(lambda x: x.serialize(), search)) # search.map((item)=>{item.serialize()})
    print("valor de search_serialize ", search_serialize)
    
    return jsonify(search_serialize), 200

@app.route('/favorite-people-user', methods=['POST'])
def get_favorite_people_user():
    '''
    Esta función va a devolver la lista de personajes favoritos de un usuario en particular
    '''
    body = request.get_json()
    print("body: ", body)
    email = body["email"]

    try:
        search = User.query.filter_by(email=email).first()
        search = search.serialize()
        print("search: ", search)

        id = search["id"]

        search2 = FavoritePeople.query.filter_by(user_id = id).all()

        search2_serialize = list(map(lambda x: x.serialize(), search2))
        print("resultado final: ", search2_serialize)

        return jsonify(search2_serialize), 200
    
    except Exception as error:
        print(str(error))
        return jsonify(str(error)), 400

@app.route('/favorite-people-user-id', methods=['POST'])
def get_favorite_people_user_id():
    '''
    Esta función va a devolver la lista de personajes favoritos de un usuario en particular por su id
    '''
    body = request.get_json()
    print("body: ", body)
    id = body["id"]

    try:      
        search2 = FavoritePeople.query.filter_by(user_id = id).all()
        search2_serialize = list(map(lambda x: x.serialize(), search2))
        print("resultado final: ", search2_serialize)
        
        return jsonify(search2_serialize), 200
    
    except Exception as error:
        print(str(error))
        return jsonify(str(error)), 400   
    

@app.route('/favorite-people-register', methods=['POST'])
def post_favorite_people_register():
    '''
    Esta función va a devolver un mensaje si se registró correctamente un favorito de un usuario
    '''
    body = request.get_json()
    print("body: ", body)
    id = body["id"]
    people_id = body["people_id"]

    try:      
        search2 = FavoritePeople.query.filter_by(user_id = id, people_id=people_id).first()
        if search2:
            return jsonify({"message":"ya existe ese favorito"}), 409
        
        new_register = FavoritePeople(user_id=id, people_id=people_id)
        db.session.add(new_register)
        db.session.commit()
               
        return jsonify({"message":"Favorito registrado"}), 201
    
    except Exception as error:
        print(str(error))
        return jsonify(str(error)), 400   
    

@app.route('/favorite-people-delete', methods=['DELETE'])
def post_favorite_people_delete():
    '''
    Esta función va a eliminar un favorito de un usuario por su id
    '''
    body = request.get_json()
    print("body: ", body)
    id = body["id"]
    people_id = body["people_id"]

    try:      
        search2 = FavoritePeople.query.filter_by(user_id = id, people_id=people_id).first()
        if not search2:
            return jsonify({"message":"no existe el registro a eliminar"}), 409
        
        db.session.delete(search2)
        db.session.commit()
               
        return jsonify({"message":"Favorito eliminado"}), 203
    
    except Exception as error:
        print(str(error))
        return jsonify(str(error)), 400   


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
