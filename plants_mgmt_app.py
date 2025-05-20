from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")

print("Loaded Mongo URI:", mongo_uri)

client = MongoClient(mongo_uri)
db = client["plants_management"]  
plants = db["plants"]             

@app.route("/plants", methods=["GET"])
def get_all_plants():
    data = list(plants.find({}, {"_id": 0}))
    return jsonify(data), 200

@app.route("/plants", methods=["POST"])
def add_plant():
    data = request.get_json()
    required_fields = {"name", "species", "price", "stock", "sunlight_requirement"}

    if not required_fields.issubset(data):
        return jsonify({"error": "Missing fields"}), 400

    plants.insert_one(data)
    return jsonify({"message": "Plant added"}), 201

@app.route("/plants/<name>", methods=["PUT"])
def update_plant(name):
    data = request.get_json()
    result = plants.update_one({"name": name}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Plant not found"}), 404
    return jsonify({"message": "Plant updated"}), 200

@app.route("/plants/<name>", methods=["DELETE"])
def delete_plant(name):
    result = plants.delete_one({"name": name})
    if result.deleted_count == 0:
        return jsonify({"error": "Plant not found"}), 404
    return jsonify({"message": "Plant deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
