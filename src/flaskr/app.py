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
    model.content_based()
    model.collabarative_filtering()

    PEOPLE_FOLDER = os.path.join('static', 'images')
    app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

    @app.route('/')
    def index():
        return render_template('home.html')
    
    @app.route('/visualize')
    def visualize():
        full_filename = os.listdir('static/images')
        imagelist = ['images/' + image for image in full_filename]
        return render_template("images.html", imagelist = imagelist)

    @app.route('/popular', methods = ['POST','GET'])
    def popular_basedTop_Books():
        print(request.method)
        if request.method == 'GET':
            return render_template('popular.html')
        elif request.method == 'POST':
            n = request.form['n']
            result = model.popular_books(int(n))
            return render_template('popular.html',result=result,n=n)

    @app.route('/popularBasedAuthor', methods = ['POST','GET'])
    def popular_basedauthor():
        if request.method == 'GET':
            return render_template('author.html')
        elif request.method == 'POST':
            author_name = request.form["AuthorName"]
            result = model.popular_based_author(author_name)
            return render_template('author.html',result = result, author_name = author_name)

    @app.route('/popularBasedPublisher', methods = ['POST','GET'])
    def popular_basedpublisher():
        if request.method == 'GET':
            return render_template('publisher.html')
        elif request.method == 'POST':
            publisher_name = request.form["PublisherName"]
            result = model.popular_based_publisher(publisher_name)
            return render_template('publisher.html',result = result, publisher_name=publisher_name)
    
    @app.route('/contentBasedCount', methods = ['POST','GET'])
    def content_based_Count():
        if request.method == 'GET':
            return render_template('count.html')
        elif request.method == 'POST':
            book_name = request.form["CountName"]
            print(book_name)
            result = model.content_based_CountVectorizer(book_name)
            return render_template('count.html',result = result, book_name=book_name)
    
    @app.route('/contentBasedTfidf', methods = ['POST','GET'])
    def content_basedtfidf():
        if request.method == 'GET':
            return render_template('tfidf.html')
        elif request.method == 'POST':
            book_name = request.form["TfidfName"]
            result = model.content_based_tfidf(book_name)
            return render_template('tfidf.html',result = result, book_name=book_name)
    
    @app.route('/collaborativeKnn', methods = ['POST','GET'])
    def collaborative_knnbooks():
        if request.method == 'GET':
            return render_template('knn.html')
        elif request.method == 'POST':
            book_name = request.form["KnnName"]
            result = model.collabarative_knn_books(book_name)
            return render_template('knn.html',result = result, book_name=book_name)
    
    @app.route('/collaborativeItem', methods = ["POST","GET"])
    def collaborataive_item():
        if request.method == 'GET':
            return render_template('listbased.html')
        elif request.method == 'POST':
            book_name = request.form['listName']
            result = model.collabarative_item_based(book_name)
            return render_template('listbased.html', result=result, book_name=book_name)
    
    @app.route('/hybridApproach', methods = ['POST','GET'])
    def hybrid_approach():
        if request.method == 'GET':
            return render_template('hybrid.html')
        elif request.method == 'POST':
            book_name = request.form['hybrid']
            result = model.hybrid_approach(book_name)
            return render_template('hybrid.html', result=result, book_name=book_name)

    return app