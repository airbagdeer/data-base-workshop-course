from db import load_ml_movies, load_ml_ratings, load_ml_links, load_ml_genome_tags, load_ml_genome_scores, load_ml_tags

# TODO: So we have this problem where we want to limit how much movies we are loading
#  to the db so that it wont take a very long time, if I set the amount to the first 1000
#  movies, we have 6 million ratings to load, which is a lot, if we limit to 100 movies,
#  we have a million ratings, which is much better and loads fast.
load_ml_movies()
load_ml_ratings()
load_ml_links()
# This two are not really interesting honestly:
# load_ml_tags()
# load_ml_genome_tags()
# load_ml_genome_scores()

