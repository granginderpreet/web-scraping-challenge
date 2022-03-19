from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)



@app.route("/")
def index():
    dictionary = mongo.db.dictionary.find_one()
    return render_template("index.html", dictionary=dictionary)

@app.route("/scrape")
def scraper():
    dictionary = mongo.db.dictionary
    dictionary_data = scrape_mars.scrape()
    dictionary.update_one({}, {"$set": dictionary_data}, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
