import csv
import re

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=chrome_options,
                              service=ChromeService(ChromeDriverManager().install()))
    return driver


def get_genres():
    driver = get_driver()
    driver.get("https://www.imdb.com/feature/genre/?ref_=nv_ch_gr#movie")
    #  //section[@class ='ipc-page-section ipc-page-section--base']/descendant::span[text() = 'Popular movies by genre']
    movie_genre_section = driver.find_element(
        By.XPATH, "//span[text() = 'Popular movies by genre']/ancestor:"
                  ":section[@class ='ipc-page-section ipc-page-section--base']")
    genres = movie_genre_section.find_elements(By.XPATH, "//a[@class = 'ipc-chip ipc-chip--on-base-accent2']")
    return [genre.text for genre in genres]


def get_movies(genres: list):
    movies = [[]]
    movie_section: WebElement
    movie_name: str = ""
    movie_year: str = ""
    driver = get_driver()
    genres = list(set(genres))
    for genre in genres:
        url = f'https://www.imdb.com/search/title/?genres={genre}&explore=genres&title_type=movie'
        driver.get(url)
        try:

            movie_sections = driver.find_elements(By.XPATH, "//div[@class = 'lister-item mode-advanced']")
            for movie in movie_sections:
                movie_name = movie.find_element(By.XPATH, ".//h3[@class = 'lister-item-header']/a").text
                movie_year = movie.find_element(By.XPATH, ".//h3[@class = 'lister-item-header']/span[@class="
                                                                  "'lister-item-year text-muted unbold']").text
                print(f'{movie_name}: {movie_year}\n')
                movie_year_number = year_in_parentheses_to_number(movie_year)
                movies.append([genre, movie_name, movie_year_number])
        except NoSuchElementException:
            print(f'{genre} is having issues while scraping data. Continuing with next item in the list')
            continue

    return movies

def year_in_parentheses_to_number(year_str):
    # Use regular expressions to extract the numeric part
    match = re.search(r'\((\d{4})\)', year_str)
    if match:
        year_number = int(match.group(1))
        return year_number
    else:
        return None  # Return None if no valid year is found

def save_movies_as_csv(movies, filename='movies.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the header row
        csv_writer.writerow(['Genre', 'Movie Name', 'Movie Year'])

        # Write the data rows
        csv_writer.writerows(movies)
    print(f'Data saved to {filename}')


genres = get_genres()
movies = get_movies(genres)
get_movies_result = get_movies(genres)
save_movies_as_csv(get_movies_result)

print(movies)
