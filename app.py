from flask import Flask, request, render_template, jsonify
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from modules import db, Queue
import json


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

CORS(app)

queue = Queue()

@app.route("/apis")
def main():
    return render_template('index.html')

@app.route('/all', methods=['GET'])
def get_all():

    new_queue = queue.get_queue()
    return jsonify(new_queue), 200

@app.route('/next', methods=['GET'])
def get_next():

    queue.dequeue()
    new_queue = queue.get_queue()
    return jsonify(new_queue), 200


@app.route('/new', methods=['POST'])
def post_new():

    body = request.get_json()

    if type(body) != dict:
        return jsonify({"msg": "Debes ingresar un objeto"})
    if not "name" in body:
        return jsonify({"msg": "Debes ingresar un nombre"})
    if not "phone" in body:
        return jsonify({"msg": "Debes ingresar un teléfono"})
    if type(body["phone"]) != int:
        return jsonify({"msg": "Debes ingresar un numero"})
    queue.enqueue(body)
    new_queue = queue.get_queue()
    return jsonify(new_queue), 200

if __name__ == "__main__":  
    manager.run()
