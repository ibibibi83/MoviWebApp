from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(100), nullable=False)

    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        """
        Convert the Movie object into a dictionary representation.

        Returns:
            dict: A dictionary containing the movie data,
            suitable for JSON serialization.
        """
        return {
            "id": self.id,
            "name": self.name,
            "director": self.director,
            "year": self.year,  # Date → string (JSON-safe)
            "poster_url": self.poster_url,
            "user_id": self.user_id
        }

