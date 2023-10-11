from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FavoritePeople(db.Model):
    __tablename__ = "favoritepeople"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "email":  User.query.get(self.user_id).serialize()["email"],
            "people_name": People.query.get(self.people_id).serialize()["name"]
        }
    
class FavoritePlanets (db.Model):
    __tablename__ = "favoriteplanets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets_id": self.planets_id,
            "email":  User.query.get(self.user_id).serialize()["email"],
            "planets_name": People.query.get(self.planets_id).serialize()["name"]
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_people = db.relationship(FavoritePeople, backref = 'user', lazy=True)
    favorite_planets = db.relationship(FavoritePlanets, backref = 'user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(30), unique=True, nullable=False)
    eye_color = db.Column(db.String(30), unique=False, nullable=True)
    hair_color = db.Column(db.String(30), unique=False, nullable=True)
    height = db.Column(db.Float, unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.String(30), unique=False, nullable=True, default="N/A")
    favorite_people = db.relationship(FavoritePeople, backref = 'people')

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "eye_color":self.eye_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "age": self.age,
            "gender": self.gender
        }
    
class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer,  primary_key=True)
    name= db.Column(db.String(30), unique=True, nullable=False)
    diameter= db.Column(db.String(30), unique=False, nullable=True)
    rotation_period= db.Column(db.String(30), unique=False, nullable=False)
    orbital_period= db.Column(db.String(30), unique=True, nullable=True)
    gravity= db.Column(db.Float, unique=True, nullable=True)
    population= db.Column(db.Integer, unique=True, nullable=True)
    climate= db.Column(db.String(30), unique=True, nullable=True)
    terrain= db.Column(db.String(50), unique=True, nullable=True)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return{

            "id": self.id,
            "name": self.name,
            "diameter":self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate, 
            "terrain": self.terrain 
        }


