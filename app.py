import os
from flask import Flask, render_template, redirect, request, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.secret_key = 'key_secret'


app.config["MONGO_DBNAME"] = 'cookbook'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-u1lvc.mongodb.net/cookbook?retryWrites=true&w=majority'
                           
mongo = PyMongo(app)


@app.route('/')
@app.route('/find_recipes')
def find_recipes():
    return render_template("index.html", recipes=mongo.db.recipes.find())


@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())


@app.route('/add_recipes')
def add_recipes():
    return render_template("add_recipe.html", categories=mongo.db.categories.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    """Creating a recipe and adding it into recipe collection"""
    
    if request.method == "POST":
        recipes = mongo.db.recipes
        recipes.insert_one(request.form.to_dict())
    
        flash("Thank you for adding a recipe!")
        
        return render_template("add_recipe.html", categories=mongo.db.categories.find())


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    return render_template("edit_recipe.html", recipe=the_recipe, categories=all_categories)


@app.route('/delete_recipe')
def delete_recipe():
    """Allow users to delete recipes"""
    return render_template("delete_recipe.html", categories=mongo.db.categories.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
