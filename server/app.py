#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def home():
    return "<h1>Zoo app</h1>"


@app.route("/animal/<int:id>")
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()

    if not animal:
        response_body = "<h1>404 Animal not found</h1>"
        response = make_response(response_body, 404)
        return response

    response_body = f"""
        <ul>
            <li style="list-style-type: none;">ID: {animal.id}</li>
            <li style="list-style-type: none;">Name: {animal.name}</li>
            <li style="list-style-type: none;">Species: {animal.species}</li>
            <li style="list-style-type: none;">Zookeeper: {animal.zookeeper.name}</li>
            <li style="list-style-type: none;">Enclosure: {animal.enclosure.environment}</li>
        </ul>
    """

    response = make_response(response_body, 200)

    return response


@app.route("/zookeeper/<int:id>")
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    if not zookeeper:
        response_body = "<h1>404 Zookeeper not found</h1>"
        response = make_response(response_body, 404)
        return response

    response_body = "<ul>"
    response_body += f"""
        <li style="list-style-type: none;">ID: {zookeeper.id}</li>
        <li style="list-style-type: none;">Zookeeper: {zookeeper.name}</li>
        <li style="list-style-type: none;">Birthday: {zookeeper.birthday}</li>
    """

    animals = [animal for animal in zookeeper.animals]

    if not animals:
        response_body += f"""<li style="list-style-type: none;">{zookeeper.name} has no animals at this time.</li>"""

    else:
        for animal in animals:
            response_body += f"""
                    <li style="list-style-type: none;">Animal: {animal.name}</li>
                """

    response_body += "</ul"

    response = make_response(response_body, 200)

    return response


@app.route("/enclosure/<int:id>")
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()

    if not enclosure:
        response_body = "<h1>404 enclosure not found</h1>"
        response = make_response(response_body, 404)
        return response

    response_body = "<ul>"
    response_body += f"""
        <li style="list-style-type: none;">ID: {enclosure.id}</li>
        <li style="list-style-type: none;">Environment: {enclosure.environment}</li>
        <li style="list-style-type: none;">Open to Visitorys: {enclosure.open_to_visitors}</li>
    """

    animals = [animal for animal in enclosure.animals]

    if not animals:
        response_body += f"""<li style="list-style-type: none;">Enclosure has no animals at this time.</li>"""

    else:
        for animal in animals:
            response_body += f"""
                    <li style="list-style-type: none;">Animal: {animal.name}</li>
                """

    response_body += "</ul"

    response = make_response(response_body, 200)

    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
