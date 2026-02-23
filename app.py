from flask import Flask, request, render_template, redirect,jsonify,url_for
from data_manager import DataManager
from models import db, User, Movie
import os
from omdb_manager import fetch_movie_data
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager()

@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def post_user():
    name = request.form.get('name')

    if not name:
        return "Name is missing", 400
    new_user = User(name=name)
    data_manager.create_user(new_user)
    return redirect('/')

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    movies = data_manager.get_movies(user_id)
    user = data_manager.get_user(user_id)
    return render_template("movies.html", user=user,movies=movies)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie_to_user(user_id):
    title = request.form.get('title')
    if not title:
        return jsonify({"error": "title is missing"}), 400
    api_data = fetch_movie_data(title)
    #print(api_data)
    if api_data:
        movie = Movie(name =api_data.get("title"), director =api_data.get("director"), year =api_data.get("year"), poster_url =api_data.get("poster"), user_id =user_id)
        data_manager.add_movie(movie)
        return redirect(f'/users/{user_id}/movies')
    movies = data_manager.get_movies(user_id)
    user = data_manager.get_user(user_id)
    return render_template("movies.html", movie_not_found =True,user=user,movies=movies)
@app.route('/movies/<int:movie_id>/update', methods=['PUT'])
def update_user_movie(movie_id):
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is missing"}), 400
    movie = data_manager.update_movie(movie_id, data["name"])
    return jsonify(movie.to_dict()), 200

@app.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_user_movie(movie_id):
    print(f"trying to delete movie movie_id")
    if data_manager.delete_movie(movie_id):
        return redirect(request.referrer or url_for("index"))
    else:
        return jsonify({"error": "error deleted movie"}), 400



if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run()