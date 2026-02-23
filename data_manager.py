from models import db, User, Movie

class DataManager():
    def create_user(self, user):
        db.session.add(user)
        db.session.commit()

    def get_users(self):
        #Gibt
        # eine
        # Liste
        # aller
        # Nutzer in deiner
        # Datenbank
        # zurück.
        return User.query.all()
    def get_user(self, id):
        user = db.session.get(User, id)
        return user


    def get_movies(self, user_id):
        """
        Retrieve all movies that belong to a specific user.

        Args:
            user_id (int): The unique ID of the user whose movies
                should be retrieved.

        Returns:
            list[Movie]: A list of Movie objects associated with
                the given user. Returns an empty list if the user
                has no movies.
        """
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """
        Add a new movie to the database.

        Args:
            movie (Movie): A Movie instance to be persisted in
                the database. The object must already contain
                all required fields (e.g. title, user_id).

        Returns:
            Movie: The newly created Movie object after it has
                been committed to the database.
        """
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, new_title,):
        """
        Update the title of an existing movie.

        Args:
            movie_id (int): The unique ID of the movie to update.
            new_title (str): The new title to assign to the movie.

        Returns:
            Movie | None: The updated Movie object if the movie
                exists, otherwise None.
        """
        movie = Movie.query.get(movie_id)

        if not movie:
            return None

        movie.title = new_title
        db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        """
        Delete a movie from the database.

        Args:
            movie_id (int): The unique ID of the movie to delete.

        Returns:
            bool: True if the movie was successfully deleted,
                False if no movie with the given ID exists.
        """
        movie = Movie.query.get(movie_id)

        if not movie:
            return False

        db.session.delete(movie)
        db.session.commit()
        return True

