import os
import json
from flask import Flask
from flask import redirect, url_for, jsonify, render_template, request
from pandas import DataFrame

from models.model import Recommender_System

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if __name__ == '__main__' :
        app.run(debug=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize Recommender Systems
    model = Recommender_System()
    model.preprocess_books()
    model.preprocess_users()
    model.preprocess_ratings()
    model.merge_data()

    @app.route('/')
    def index():
        return render_template('home.html')

    @app.route('/popular', methods = ['POST','GET'])
    def popular_basedTop_Books():
        print(request.method)
        if request.method == 'GET':
            return render_template('popular.html')
        elif request.method == 'POST':
            n = request.form['n']
            result = model.popular_books(int(n))
            return render_template('popular.html',result=result,n=n)


    return app

