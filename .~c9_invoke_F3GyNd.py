import os
import sys
import request
import json
import utils
import rekognize
from flask import Flask, render_template, redirect, url_for, request, session
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy


# EB looks for an 'application' callable by default.
application = Flask(__name__)

# Configurations
application.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(application)
from models import *

@application.route('/')
def index():
    datasets = Dataset.query.all()
    return render_template("index.html", 
                           datasets=datasets)


@application.route('/search')
def search():
    return render_template("search.html")
    
@application.route('/new', )
def new():
    return render_template("form.html")
    
@application.route('/add', methods=['GET', 'POST'])
def process_data():
    try:
        name =  request.form['name']
        description = request.form['description']
        image = request.files['image']
        
        print "getting data from image..."
        try:
            rekognize.analyze(image, image.filename)
        except Exeption as e:
            
            print 'Failed to add image: Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
        
        dataset = Dataset(name, description, "data")
        db.session.add(dataset)
        db.session.commit()
    except Exception as e:
        print 'Failed to add image: Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
        pass
    return redirect(url_for('index'))

# run the app.
if __name__ == "__main__":
    # Build the database:
    # This will create the database file using SQLAlchemy
    db.create_all()
    
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
