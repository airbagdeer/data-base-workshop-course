# import requests
# import time

# TMDB_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NmM1ZDI1YjAzOWNkMTg1NDkzNWI4N2I2NWYyYTI4MyIsIm5iZiI6MTc2NjQzMzYyMS4wOTc5OTk4LCJzdWIiOiI2OTQ5YTM1NTQ3YWQzOTJhYWE4ZWJmMGYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.mdQsRpAI5Hi45y2JK4uQ54qR0DjOuqDk92LfUAHs8Lc"

# SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

# HEADERS = {
#     "Authorization": f"Bearer {TMDB_BEARER_TOKEN}",
#     "Content-Type": "application/json;charset=utf-8"
# }

# def get_movie_id(title):
#     params = {
#         "query": title,
#         "include_adult": False,
#         "language": "en-US",
#         "page": 1
#     }

#     response = requests.get(SEARCH_URL, headers=HEADERS, params=params)
#     response.raise_for_status()
#     data = response.json()

#     if data["results"]:
#         return data["results"][0]["id"]
#     return None


# def fetch_movie_ids(movie_titles):
#     ids = []

#     for title in movie_titles:
#         movie_id = get_movie_id(title)
#         ids.append(movie_id)
#         time.sleep(0.25)  # respect rate limits

#     return ids


# if __name__ == "__main__":
#     educational_movies = [
#     # Science, Math, Physics
#     "A Beautiful Mind",
#     "The Theory of Everything",
#     "The Imitation Game",
#     "The Man Who Knew Infinity",
#     "Particle Fever",
#     "The Farthest",
#     "Cosmos",
#     "Apollo 13",
#     "First Man",
#     "The Right Stuff",
#     "October Sky",
#     "The Martian",
#     "Contact",
#     "Arrival",
#     "Pi",
#     "Primer",
#     "Interstellar",
#     "Gravity",
#     "Einstein and Eddington",
#     "Hawking",

#     # Technology, AI, Computing
#     "AlphaGo",
#     "Coded Bias",
#     "The Social Dilemma",
#     "The Great Hack",
#     "Inside Bill's Brain",
#     "Ex Machina",
#     "Her",
#     "Snowden",
#     "WarGames",
#     "Hackers",
#     "Citizenfour",
#     "Terms and Conditions May Apply",
#     "Lo and Behold, Reveries of the Connected World",
#     "The Internet's Own Boy",
#     "Codebreaker",
#     "Tron",
#     "Ready Player One",
#     "We Are Legion: The Story of the Hacktivists",
#     "The Code",

#     # Economics, Finance, Business
#     "The Big Short",
#     "Inside Job",
#     "Margin Call",
#     "Moneyball",
#     "Enron: The Smartest Guys in the Room",
#     "Too Big to Fail",
#     "Capital in the Twenty-First Century",
#     "Freakonomics",
#     "The Ascent of Money",
#     "Becoming Warren Buffett",
#     "Dirty Money",
#     "American Factory",
#     "The Founder",
#     "Startup.com",
#     "Something Ventured",
#     "Betting on Zero",
#     "Saving Capitalism",
#     "Inequality for All",
#     "Commanding Heights",

#     # Politics, Media, Society
#     "13th",
#     "All the President's Men",
#     "Spotlight",
#     "The Post",
#     "The Fog of War",
#     "Hotel Rwanda",
#     "Schindler's List",
#     "The Pianist",
#     "The Act of Killing",
#     "The Look of Silence",
#     "No End in Sight",
#     "Restrepo",
#     "Fahrenheit 9/11",
#     "Why We Fight",
#     "The Square",
#     "Collective",
#     "The Dissident",
#     "Navalny",
#     "Winter on Fire",

#     # Psychology, Sociology, Behavior
#     "The Stanford Prison Experiment",
#     "Three Identical Strangers",
#     "Crazy, Not Insane",
#     "Mind Games",
#     "Human Nature",
#     "The Brain with David Eagleman",
#     "Free Solo",
#     "Touching the Void",
#     "The Dawn Wall",
#     "Man on Wire",
#     "Jiro Dreams of Sushi",
#     "Abstract: The Art of Design",
#     "Helvetica",
#     "Exit Through the Gift Shop",
#     "The Social Animal",
#     "Happy",
#     "Minimalism",
#     "Samsara",

#     # Biology, Medicine, Health
#     "Contagion",
#     "Pandemic: How to Prevent an Outbreak",
#     "The Immortal Life of Henrietta Lacks",
#     "Unrest",
#     "Awake: The Life of Yogananda",
#     "My Octopus Teacher",
#     "Life Itself",
#     "The Cove",
#     "Blackfish",
#     "Forks Over Knives",
#     "What the Health",
#     "Food, Inc.",
#     "Supersize Me",
#     "Fat, Sick & Nearly Dead",
#     "Heal",
#     "Living Proof",
#     "Sicko",
#     "And the Band Played On",

#     # Environment, Climate, Earth
#     "An Inconvenient Truth",
#     "An Inconvenient Sequel",
#     "Before the Flood",
#     "Our Planet",
#     "Chasing Ice",
#     "Chasing Coral",
#     "Kiss the Ground",
#     "Home",
#     "Planet Earth",
#     "Earthlings",
#     "The 11th Hour",
#     "A Plastic Ocean",
#     "Seaspiracy",
#     "Cowspiracy",
#     "The Biggest Little Farm",
#     "Ice on Fire",
#     "Blue Planet",
#     "Virunga",

#     # Education & Learning
#     "Waiting for Superman",
#     "The Class",
#     "To Be and to Have",
#     "Spellbound",
#     "Science Fair",
#     "Most Likely to Succeed",
#     "Race to Nowhere",
#     "Teach Us All",
#     "Ivory Tower",
#     "First Position",

#     # History & Civilization
#     "Shoah",
#     "They Shall Not Grow Old",
#     "The Civil War",
#     "The Vietnam War",
#     "The World at War",
#     "Night and Fog",
#     "The Great War",
#     "Rome: Engineering an Empire",
#     "Ancient Aliens",
#     "Guns, Germs and Steel",
#     "The Story of Maths",
#     "The Story of Science",
#     "Connections",
#     "Civilisation",
#     "The Ascent of Man"
#     ]

#     movie_ids = fetch_movie_ids(educational_movies)

#     print(movie_ids)



import requests
import time

TMDB_BEARER_TOKEN = "enter-your-tmdb-bearer-token-here"

SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DETAILS_URL = "https://api.themoviedb.org/3/movie/{}"

HEADERS = {
    "Authorization": f"Bearer {TMDB_BEARER_TOKEN}",
    "Content-Type": "application/json;charset=utf-8"
}

def get_imdb_id(title):
    # Search for the movie in TMDb
    params = {
        "query": title,
        "include_adult": False,
        "language": "en-US",
        "page": 1
    }
    response = requests.get(SEARCH_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    if not data["results"]:
        return None

    tmdb_id = data["results"][0]["id"]

    # Fetch movie details to get IMDb ID
    response = requests.get(MOVIE_DETAILS_URL.format(tmdb_id), headers=HEADERS)
    response.raise_for_status()
    movie_data = response.json()

    return movie_data.get("imdb_id")


def fetch_imdb_ids(movie_titles):
    imdb_ids = []
    for title in movie_titles:
        imdb_id = get_imdb_id(title)
        imdb_ids.append(imdb_id)
        time.sleep(0.25)  # respect rate limits
    return imdb_ids


if __name__ == "__main__":
    educational_movies = [
    # Science, Math, Physics
    "A Beautiful Mind",
    "The Theory of Everything",
    "The Imitation Game",
    "The Man Who Knew Infinity",
    "Particle Fever",
    "The Farthest",
    "Cosmos",
    "Apollo 13",
    "First Man",
    "The Right Stuff",
    "October Sky",
    "The Martian",
    "Contact",
    "Arrival",
    "Pi",
    "Primer",
    "Interstellar",
    "Gravity",
    "Einstein and Eddington",
    "Hawking",

    # Technology, AI, Computing
    "AlphaGo",
    "Coded Bias",
    "The Social Dilemma",
    "The Great Hack",
    "Inside Bill's Brain",
    "Ex Machina",
    "Her",
    "Snowden",
    "WarGames",
    "Hackers",
    "Citizenfour",
    "Terms and Conditions May Apply",
    "Lo and Behold, Reveries of the Connected World",
    "The Internet's Own Boy",
    "Codebreaker",
    "Tron",
    "Ready Player One",
    "We Are Legion: The Story of the Hacktivists",
    "The Code",

    # Economics, Finance, Business
    "The Big Short",
    "Inside Job",
    "Margin Call",
    "Moneyball",
    "Enron: The Smartest Guys in the Room",
    "Too Big to Fail",
    "Capital in the Twenty-First Century",
    "Freakonomics",
    "The Ascent of Money",
    "Becoming Warren Buffett",
    "Dirty Money",
    "American Factory",
    "The Founder",
    "Startup.com",
    "Something Ventured",
    "Betting on Zero",
    "Saving Capitalism",
    "Inequality for All",
    "Commanding Heights",

    # Politics, Media, Society
    "13th",
    "All the President's Men",
    "Spotlight",
    "The Post",
    "The Fog of War",
    "Hotel Rwanda",
    "Schindler's List",
    "The Pianist",
    "The Act of Killing",
    "The Look of Silence",
    "No End in Sight",
    "Restrepo",
    "Fahrenheit 9/11",
    "Why We Fight",
    "The Square",
    "Collective",
    "The Dissident",
    "Navalny",
    "Winter on Fire",

    # Psychology, Sociology, Behavior
    "The Stanford Prison Experiment",
    "Three Identical Strangers",
    "Crazy, Not Insane",
    "Mind Games",
    "Human Nature",
    "The Brain with David Eagleman",
    "Free Solo",
    "Touching the Void",
    "The Dawn Wall",
    "Man on Wire",
    "Jiro Dreams of Sushi",
    "Abstract: The Art of Design",
    "Helvetica",
    "Exit Through the Gift Shop",
    "The Social Animal",
    "Happy",
    "Minimalism",
    "Samsara",

    # Biology, Medicine, Health
    "Contagion",
    "Pandemic: How to Prevent an Outbreak",
    "The Immortal Life of Henrietta Lacks",
    "Unrest",
    "Awake: The Life of Yogananda",
    "My Octopus Teacher",
    "Life Itself",
    "The Cove",
    "Blackfish",
    "Forks Over Knives",
    "What the Health",
    "Food, Inc.",
    "Supersize Me",
    "Fat, Sick & Nearly Dead",
    "Heal",
    "Living Proof",
    "Sicko",
    "And the Band Played On",

    # Environment, Climate, Earth
    "An Inconvenient Truth",
    "An Inconvenient Sequel",
    "Before the Flood",
    "Our Planet",
    "Chasing Ice",
    "Chasing Coral",
    "Kiss the Ground",
    "Home",
    "Planet Earth",
    "Earthlings",
    "The 11th Hour",
    "A Plastic Ocean",
    "Seaspiracy",
    "Cowspiracy",
    "The Biggest Little Farm",
    "Ice on Fire",
    "Blue Planet",
    "Virunga",

    # Education & Learning
    "Waiting for Superman",
    "The Class",
    "To Be and to Have",
    "Spellbound",
    "Science Fair",
    "Most Likely to Succeed",
    "Race to Nowhere",
    "Teach Us All",
    "Ivory Tower",
    "First Position",

    # History & Civilization
    "Shoah",
    "They Shall Not Grow Old",
    "The Civil War",
    "The Vietnam War",
    "The World at War",
    "Night and Fog",
    "The Great War",
    "Rome: Engineering an Empire",
    "Ancient Aliens",
    "Guns, Germs and Steel",
    "The Story of Maths",
    "The Story of Science",
    "Connections",
    "Civilisation",
    "The Ascent of Man"
    ]

    imdb_ids = fetch_imdb_ids(educational_movies)
    print(imdb_ids)
