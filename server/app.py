from flask import Flask, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

migrate = Migrate(app, db)
api = Api(app)


class Plants(Resource):
    def get(self):
        return [plant.to_dict() for plant in Plant.query.all()], 200

    def post(self):
        data = request.get_json()
        plant = Plant(
            name=data["name"],
            image=data["image"],
            price=data["price"]
        )
        db.session.add(plant)
        db.session.commit()
        return plant.to_dict(), 201


class PlantByID(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return {}, 404
        return plant.to_dict(), 200

    def patch(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return {}, 404
        data = request.get_json()
        if "name" in data:
            plant.name = data["name"]
        if "image" in data:
            plant.image = data["image"]
        if "price" in data:
            plant.price = data["price"]
        if "is_in_stock" in data:
            plant.is_in_stock = data["is_in_stock"]
        db.session.commit()
        return plant.to_dict(), 200

    def delete(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return {}, 404
        db.session.delete(plant)
        db.session.commit()
        return "", 204


api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
