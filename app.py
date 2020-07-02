import os
import math
from flask import Flask, render_template, redirect, request, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.secret_key = 'key_secret'


app.config["MONGO_DBNAME"] = 'cookbook'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-u1lvc.mongodb.net/cookbook?retryWrites=true&w=majority'
                           
mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
# Home page shows 'welcome' text
def index():
    return render_template("index.html", title="Home", recipes=mongo.db.recipes.find())


@app.route('/get_recipes')
# Displaying recipes collection with a choice of categories 
def get_recipes():
    # Logic for pagination
    per_page = 8
    page = int(request.args.get('page', 1))
    total = mongo.db.recipes.count_documents({})
    all_recipes = mongo.db.recipes.find().skip((page - 1) * per_page).limit(per_page)
    pages = range(1, int(math.ceil(total / per_page)) + 1)
    return render_template("recipes.html", title="Recipes", recipes=all_recipes, page=page, pages=pages, total=total)


@app.route('/add_recipes')
# User can create a recipe and it will be added into recipe collection
def add_recipes():
    return render_template("add_recipe.html", title="Add Recipe", categories=mongo.db.categories.find())


@app.route('/fruit_smoothies')
# Route to the category of fruit smoothies
def fruit_smoothies():
    # Logic for pagination
    per_page = 8
    page = int(request.args.get('page', 1))
    total = mongo.db.recipes.count_documents({})
    recipes = mongo.db.recipes.find({'category_name': 'Fruit smoothie'}).skip((page - 1) * per_page).limit(per_page)
    pages = range(1, int(math.ceil(total / per_page)) + 1)
    return render_template("recipes.html", title="Fruit Smoothies", recipes=recipes, page=page, pages=pages, total=total)


@app.route('/green_smoothies')
# Route to the category of green smoothies
def green_smoothies():
    # Logic for pagination
    per_page = 8
    page = int(request.args.get('page', 1))
    total = mongo.db.recipes.count_documents({})
    recipes = mongo.db.recipes.find({'category_name': 'Green smoothie'}).skip((page - 1) * per_page).limit(per_page)
    pages = range(1, int(math.ceil(total / per_page)) + 1)
    return render_template("recipes.html", title="Green Smoothies", recipes=recipes, page=page, pages=pages, total=total)


@app.route('/protein_smoothies')
# Route to the category of protein smoothies
def protein_smoothies():
    # Logic for pagination
    per_page = 8
    page = int(request.args.get('page', 1))
    total = mongo.db.recipes.count_documents({})
    recipes = mongo.db.recipes.find({'category_name': 'Protein smoothie'}).skip((page - 1) * per_page).limit(per_page)
    pages = range(1, int(math.ceil(total / per_page)) + 1)
    return render_template("recipes.html", title="Protein Smoothies", recipes=recipes, page=page, pages=pages, total=total)


@app.route('/blenders')
# Displaying blenders collection with a link to the shop 
def blenders():
    return render_template("blenders.html", title="Blenders", blenders=mongo.db.blenders.find())


@app.route('/insert_recipe', methods=['POST'])
# The route to the form for inserting created recipe
def insert_recipe():
    if request.method == "POST":
        recipes = mongo.db.recipes
        recipes.insert_one(request.form.to_dict())
        flash("Thank you for adding a recipe!")
        return render_template("add_recipe.html", categories=mongo.db.categories.find())


@app.route('/edit_recipe/<recipe_id>')
# The route to the form for editing existing recipe
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    return render_template("edit_recipe.html", title="Edit Recipe", recipe=the_recipe, categories=all_categories)


@app.route('/update_recipe/<recipe_id>', methods=['POST'])
# The route to the form for inserting updated recipe
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)}, {   
        'recipe_name': request.form.get('recipe_name'),
        'category_name': request.form.get('category_name'),
        'ingredients': request.form.get('ingredients'),
        'instruction': request.form.get('instruction'),
        'recipe_image': request.form.get('recipe_image'),
        'source': request.form.get('source')
    })
    return redirect(url_for('get_recipes'))


@app.route('/delete_recipe/<recipe_id>', methods=['POST'])
# The route to delete the existing recipe. The recipe will be deleted from the database
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', 5000)),
            debug=False)
