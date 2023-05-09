import json

class MovieStorage:
    def __init__(self, file_path):
        self.file_path = file_path
        self.movies = self.load_movies()

    def load_movies(self):
        try:
            with open(self.file_path, 'r') as file:
                movies = json.load(file)
        except FileNotFoundError:
            movies = {}
        return movies

    def save_movies(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.movies, file)

    def add_movie(self, title, year, rating, poster):
        self.movies[title] = {'year': year, 'rating': rating, 'poster': poster}
        self.save_movies()

    def delete_movie(self, title):
        if title in self.movies:
            del self.movies[title]
            self.save_movies()
            return True
        else:
            return False

    def update_movie(self, title, rating):
        if title in self.movies:
            self.movies[title]['rating'] = rating
            self.save_movies()
            return True
        else:
            return False

    def list_movies(self):
        return self.movies
