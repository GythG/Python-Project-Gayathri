import pandas as pd


# Function to read the CSV file and filter movies by genre
def interactive_movie_search(csv_filename):
    movies = pd.read_csv(csv_filename)
    genres = movies['Genre'].unique()

    print("\n\n***********************MOVIE SUGGESTION BOT**********************************\n")
    print("Welcome to Movie suggestions bot..!\n")

    while True:
        print("Please choose a genre from the below to get top suggestions...!\n")
        print(genres)
        genre_input = input("\nEnter a genre (or type 'bye' to exit): ")

        if genre_input.lower() == 'bye':
            print("Thank you for using Movie Suggestion bot!")
            break

        genre_movies = movies[movies['Genre'].str.lower() == genre_input.lower()]

        if genre_movies.empty:
            print(f"No movies found for the genre '{genre_input}'.")
        else:
            # Sort by the 'Movie Name' column and display the top 10
            # genre_movies_sorted = genre_movies.sort_values(by='Movie Name').head(10)
            genre_movies_sorted = genre_movies.head(10)
            print("Top 10 movies in this genre:\n")
            for i, row in genre_movies_sorted.iterrows():
                print(f"{row['Movie Name']} ({int(row['Movie Year'])})")
        print("***************************ENJOY WATCHING**************************************\n")

# Example usage:
# Specify the filename of your CSV file containing the movie data
csv_filename = 'movies.csv'
interactive_movie_search(csv_filename)
