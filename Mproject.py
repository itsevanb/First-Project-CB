# Import modules at the beginning of the script
import json
import movie_storage as ms
import requests
import random
from rapidfuzz import fuzz
import matplotlib.pyplot as plt


class Colors:
    """Create a class to store colors for the terminal"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[35m'
    END = '\033[0m'


def menu_choice():
    print(f'\n{Colors.BLUE}Movie Menu:{Colors.END}')
    print('0. Exit the application')
    print('1. List all movies')
    print('2. Add movie')
    print('3. Delete movie')
    print('4. Update movie')
    print('5. Movie Stats')
    print('6. Pick a random movie')
    print('7. Search for a movie')
    print('8. Sort movies by rating')
    print('9. Display Graph of Movies')
    print('10. Generate movie data base website')
    try:
        choice = int(input(f'{Colors.PURPLE}\nEnter choice (0-10): {Colors.END}'))
        if 0 <= choice <= 10:
            return choice
        else:
            print(f"{Colors.RED}Invalid choice. Please try again with values (0-10).{Colors.END}")
    except ValueError:
        print(f"{Colors.RED}Invalid choice. Please try again with values (0-10).{Colors.END}")

def welcome():
    print(f"{Colors.GREEN}******************Welcome to our Movie Database!*********************{Colors.END}")
    print("\n\nPlease chose an option from our 'Movie Menu' below:")

def movie_list():
    movie_dict = movie_storage.list_movies()
    for title, properties in movie_dict.items():
        print(f"{title}: {properties['rating']}, {properties['year']}")

def fetch_movie_data(title):
    api_key = 'a1c766c0'
    url = f'http://www.omdbapi.com/?apikey={api_key}&t={title}'
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        return None
    
    data = response.json()
    if data['Response'] == 'True':
        movie_data = {'title': data['Title'],
                      'year': data['Year'],
                      'rating': data['imdbRating'],
                      'poster': data['Poster'] 
                      }
        return movie_data
    else:
        print(f"{Colors.RED}Movie not found. Please try again.{Colors.END}")
        return None

def add_movie():
    title = input(f'{Colors.PURPLE}Please enter a movie title: {Colors.END}')
    movie_data = fetch_movie_data(title)
    if movie_data:
        movie_storage.add_movie(movie_data['title'], movie_data['year'], movie_data['rating'], movie_data['poster'])
        print(f"Movie '{movie_data['title']}' has been added.")
        save_movies(movie_storage.list_movies())

def delete_movie():
    title = input(f'{Colors.PURPLE}Please enter the title of the movie you would like to delete: {Colors.END}')
    if movie_storage.delete_movie(title):
        print(f"Movie '{title}' has been deleted.")
        save_movies(movie_storage.list_movies())
    else:
        print(f"Movie not found in database")

def movie_update():
    title = input(f'{Colors.PURPLE}Please enter a movie title to update: {Colors.END}')
    if title in movie_storage.list_movies():
        rating = float(input(f'{Colors.PURPLE}Please enter a new rating for the movie: {Colors.END}'))
        movie_storage.update_movie(title, rating)
        print(f"Movie '{title}' has been updated.")
        save_movies(movie_storage.list_movies())
    else:
        print(f"Movie not found in database")

def movie_stats(movie_dict):
    if not movie_dict:
        print("No movies in the database")
        return
    ratings = [float(properties['rating']) for properties in movie_dict.values()]  # Fixed the extraction of ratings
    total_movies = len(ratings)
    avg_rating = sum(ratings) / total_movies
    sorted_ratings = sorted(ratings)
    med_rating = (sorted_ratings[(total_movies - 1) // 2] + sorted_ratings[total_movies // 2]) / 2  # Simplified the median calculation
    best_rating = max(ratings)
    worst_rating = min(ratings)
    best_movies = [title for title, properties in movie_dict.items() if properties['rating'] == best_rating]
    worst_movies = [title for title, properties in movie_dict.items() if properties['rating'] == worst_rating]
    print(f"Total movies: {total_movies}")
    print(f"Average movie rating: {avg_rating:.2f}")
    print(f"Median rating: {med_rating:.2f}")
    print("Best movie(s): ")
    for movie in best_movies:
        print(f"{movie}: {best_rating}")
    print("Worst_movie(s): ")
    for movie in worst_movies:
        print(f"{movie}: {worst_rating}")

def random_movie(movie_dict):
    title = random.choice(list(movie_dict.keys()))
    movie_properties = movie_dict[title]
    print(f"{title}: came out in {movie_properties['year']} with a rating of {movie_properties['rating']}")

def movie_search(movie_dict, search_query):
    search_query_lower = search_query.lower()
    matching_movies = [title for title, properties in movie_dict.items() if fuzz.partial_ratio(search_query_lower, title.lower()) > 80]
    exact_match = [title for title, properties in movie_dict.items() if fuzz.partial_ratio(search_query_lower, title.lower()) == 100]
    if exact_match:
        print(f"Movie found: {exact_match[0]}")
    elif matching_movies:
        print(f"The movie '{search_query}' was not found in the database, but did you mean: ")
        for title in matching_movies:
            print(f"{title}: {movie_dict[title]['rating']}, {movie_dict[title]['year']}")
    else:
        print(f"No movies found containing {search_query}")


def graph_movie(movie_dict, file_name):
    ratings = [properties['rating'] for properties in movie_dict.values()]
    bins = range(0, 11)
    plt.hist(ratings, bins, color='green')
    plt.xlabel("Ratings")
    plt.ylabel("Frequency")
    plt.title("Movie Ratings Visualized")
    plt.xticks(bins)
    plt.tight_layout()
    plt.savefig(file_name)
    plt.show()

def movie_rating(movie_dict):
    #sort movies by rating
    sorted_movies = sorted(movie_dict.items(), key=lambda x: float(x[1]['rating']), reverse=True)  
    for title, properties in sorted_movies:
        print(f"{title}: {properties['rating']}")

def save_movies(movie_dict):
    with open('movie_data.json', 'w') as file:
        json.dump(movie_dict, file, indent=4)

def generate_html(movie_dict):
    with open('index.html', 'r') as file:
        index_html = file.read()
    movie_grid = ''
    for title, properties in movie_dict.items():
        movie_grid += f'<li><strong>{title}</strong> ({properties["year"]}): {properties["rating"]}</li>'

    html_content = index_html.replace("__TEMPLATE_TITLE__", "Evan's Movie Database")
    html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
    return html_content
    
def main():
    welcome()
    while True:
        choice = menu_choice()
        if choice == 1:
            movie_list()
        elif choice == 2:
            add_movie()
        elif choice == 3:
            delete_movie()
        elif choice == 4:
            movie_update()
        elif choice == 5:
            movie_stats(movie_storage.list_movies())
        elif choice == 6:
            random_movie(movie_storage.list_movies())
        elif choice == 7:
            search_query = input(f"{Colors.PURPLE}Please enter your movie search: {Colors.END}")
            movie_search(movie_storage.list_movies(), search_query)
        elif choice == 8:
            movie_rating(movie_storage.list_movies())
        elif choice == 9:
            file_name = input(f"{Colors.PURPLE}Please enter a file name to save the graph to (e.g. '.png' or '.jpeg'): {Colors.END}")
            graph_movie(movie_storage.list_movies(), file_name)
        elif choice == 10:
            html_content = generate_html(movie_storage.list_movies())
            with open('output.html', 'w') as file:
                file.write(html_content)
            print(f"{Colors.YELLOW}HTML file generated successfully!{Colors.END}")
        elif choice == 0:
            save_movies(movie_storage.list_movies())
            print(f"{Colors.YELLOW}Goodbye! :){Colors.END}")
            break
        else:
            print(f"{Colors.RED}Invalid choice. Please try again with values (0-10).{Colors.END}")

if __name__ == "__main__":
    movie_storage = ms.MovieStorage('movie_data.json')
    main()