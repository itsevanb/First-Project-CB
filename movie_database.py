#Create menu features for the 'movies dictionary' that implements CRUD commands

#creating a colors class, to be able to cleanly add color to the code, and do it using methods
class Colors:
  Blue = '\033[94m'
  Green = '\033[92m'
  Red = '\033[91m'
  Yellow = '\033[93m'
  Purple = '\033[35m'
  End = '\033[0m' #ANSI escape code to set terminal style back to default

#Display Menu, ask for user input
def menu_choice():
    print(f'\n{Colors.Blue}Movie Menu:{Colors.End}')
    print('1. List all movies')
    print('2. Add movie')
    print('3. Delete movie')
    print('4. Update movie')
    print('5. Movie Stats')
    print('6. Pick a random movie')
    print('7. Search for a movie')
    print('8. Sort movies by rating')
    print('9. Display Graph of Movies')
    print('10. Exit the application')
    choice = int(input(f'{Colors.Purple}\nEnter choice (1-10): {Colors.End}'))
    return choice


#welcome message to user when accessing database
def welcome():
  print(f"{Colors.Green}******************Welcome to our Movie Database!*********************{Colors.End}")
  print("\n\nPlease chose an option from our 'Movie Menu' below:")

#List all movies in dictionary
def movie_list(movie_dict):
    for title, rating in movie_dict.items():
        print(f"{title}: {rating}")


#Add the ability to add to our movies dictionary
def add_movie(movie_dict):
    title = input(f'{Colors.Purple}Please enter movie title: {Colors.End}')
    rating = float(input(f'{Colors.Purple}Please enter movie rating: {Colors.End}'))
    movie_dict[title] = rating
    print(f"Movie '{title}' was added with the applied rating of '{rating}'")


#Add the ability to delete a movie from our movie dictionary
def delete_movie(movie_dict):
    title = input(f'{Colors.Purple}Please enter the title of the movie you would like to delete: {Colors.End}')
    if title in movie_dict:
        del movie_dict[title]
        print(f"Movie '{title}' has been deleted.")
    else:
        print(f"Movie not found in database")


#Add ability to make an update to an existing movie
def movie_update(movie_dict):
    title = input(f'{Colors.Purple}Please enter a movie title to update: {Colors.End}')
    if title in movie_dict:
        rating = float(input(f'{Colors.Purple}Please enter a new rating: {Colors.End}'))
        movie_dict[title] = rating
    else:
        print(f"Movie not found in database")


# Print movie statistics in database
# 1. Average rating for all movies
# 2. Median rating for all movies // median is the middle number; if odd number just middle value, if even it is avg of two middle value(s)
# 3. The best movie ratings, if multiple print all
# 4. Worst movie ratings if multiple print all
def movie_stats(movie_dict):
    if not movie_dict:
        print(
            f"No movies in the database")  # since I am using parameters and arguments, if code is re-ran with a different dictionary as argument, this will show
        return
    ratings = list(movie_dict.values())
    total_movies = len(ratings)
    avg_rating = sum(ratings) / total_movies  # sum can be used here, when needing to add iterables rather than make a loop
    med_rating = sorted(ratings)[total_movies // 2] if total_movies % 2 != 0 else (sorted(ratings)[(total_movies - 1) // 2] + sorted(ratings)[total_movies // 2] / 2)
    best_rating = max(ratings)
    worst_rating = min(ratings)
    best_movie = [title for title, rating in movie_dict.items() if rating == best_rating]
    worst_movie = [title for title, rating in movie_dict.items() if rating == worst_rating]
    print(f"Total movies: {total_movies}")
    print(f"Average movie rating: {avg_rating:.2f}")# floating point number (x.xx)
    print(f"Median rating: {med_rating:.2f}")
    print("Best movie(s): ")
    for movie in best_movie:
        print(f"{movie}: {best_rating}")
    print("Worst_movie(s): ")
    for movie in worst_movie:
        print(f"{movie}: {worst_rating}")

#pick a random movie and its rating
import random

def random_movie(movie_dict):
    title = random.choice(list(movie_dict.keys()))
    print(f"Random movie is: {title}: {movie_dict[title]}")

#search for movie, case-INsenseitive
#Import an editing distance library
from rapidfuzz import fuzz

def movie_search(movie_dict, search_query):
    search_query_lower = search_query.lower()
    mathching_movies = [title for title, rating in movie_dict.items() if fuzz.partial_ratio(search_query_lower, title.lower()) > 80]
    exact_match = [title for title, rating in movie_dict.items() if fuzz.partial_ratio(search_query_lower, title.lower()) == 100]
    if exact_match:
        print(f"Movie found: {exact_match[0]}")
    elif mathching_movies:
        print(f"The movie '{search_query}' was not found in database, but did you mean: ")
        for title in mathching_movies:
          print(f"{title}: {movie_dict[title]}")
    else:
        print(f"No movies found containing {search_query}")

#create a histogram with dictionary dataset, ask user where to save file of the histogram
import matplotlib.pyplot as plt

def graph_movie(movie_dict, file_name):
  movies = list(movie_dict.keys())
  ratings = list(movie_dict.values())
  plt.bar(movies, ratings, color = 'green')
  plt.xlabel("Movies")
  plt.ylabel("Ratings")
  plt.title("Movie Ratings Visualized")
  plt.xticks(rotation=90)
  plt.tight_layout()
  plt.savefig(file_name)
  plt.show()

#Movies sorted by rating
def movie_rating(movie_dict):
    sorted_movies = sorted(movie_dict.items(), key=lambda x: x[1], reverse=True)
    for title, rating in sorted_movies:
        print(f"{title}: {rating}")

#Main function
def main():
    welcome()
    #Dictionary to store the movies and the rating
    movies = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 3.6,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight": 9.0,
        "12 Angry Men": 8.9,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7
    }

    while True:
        choice = menu_choice()
        if choice == 1:
            movie_list(movies)
        elif choice == 2:
            add_movie(movies)
        elif choice == 3:
            delete_movie(movies)
        elif choice == 4:
            movie_update(movies)
        elif choice == 5:
            movie_stats(movies)
        elif choice == 6:
            random_movie(movies)
        elif choice == 7:
            search_query = input(f"{Colors.Purple}Please enter your movie search: {Colors.End}")
            movie_search(movies, search_query)
        elif choice == 8:
            movie_rating(movies)
        elif choice == 9:
            file_name = input(f"{Colors.Purple}Please enter a file name to save the graph to (e.g. '.png' or '.jpeg'): {Colors.End}")
            graph_movie(movies, file_name)
        elif choice == 10:
            print(f"{Colors.Yellow}Goodbye! :){Colors.End}")
            break
        else:
            print(f"{Colors.Red}Invalid choice. Please try again with values (1-10).{Colors.End}")

if __name__ == "__main__":
    main()