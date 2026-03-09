from flask import Flask, request, render_template, redirect, jsonify, url_for
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
    """
    Render the homepage with a list of all users.

    Returns:
        HTML page displaying all users stored in the database.
    """
    try:
        users = data_manager.get_users()
        return render_template('index.html', users=users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users', methods=['POST'])
def post_user():
    """
    Create a new user.
    """
    name = request.form.get('name')

    if not name:
        return "Name is missing", 400

    try:
        new_user = User(name=name)
        data_manager.create_user(new_user)
        return redirect('/')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    """
    Display all movies belonging to a specific user.
    """
    try:
        movies = data_manager.get_movies(user_id)
        user = data_manager.get_user(user_id)
        return render_template("movies.html", user=user, movies=movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie_to_user(user_id):
    """
    Add a new movie to a user's movie list.
    """
    title = request.form.get('title')

    try:
        movies = data_manager.get_movies(user_id)
        user = data_manager.get_user(user_id)

        if not title:
            return jsonify({"error": "title is missing"}), 400

        api_data = fetch_movie_data(title)

        if api_data:

            if title.lower() == api_data.get("title").lower():
                return render_template(
                    "movies.html",
                    movie_exist=True,
                    user=user,
                    movies=movies
                )

            movie = Movie(
                name=api_data.get("title"),
                director=api_data.get("director"),
                year=api_data.get("year"),
                poster_url=api_data.get("poster"),
                user_id=user_id
            )

            data_manager.add_movie(movie, user_id)

            return redirect(f'/users/{user_id}/movies')

        return render_template(
            "movies.html",
            movie_not_found=True,
            user=user,
            movies=movies
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/movies/<int:movie_id>/update', methods=['POST'])
def update_user_movie(movie_id):
    """
    Update the name of an existing movie.
    """
    try:
        data = request.get_json()

        if not data or "name" not in data:
            return jsonify({"error": "name is missing"}), 400

        movie = data_manager.update_movie(movie_id, data["name"])

        return jsonify(movie.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_user_movie(movie_id):
    """
    Delete a movie from the database.
    """
    try:
        if data_manager.delete_movie(movie_id):
            return redirect(request.referrer or url_for("index"))
        else:
            return jsonify({"error": "error deleted movie"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    """
    Entry point of the Flask application.
    """
    with app.app_context():
        db.create_all()

    app.run()