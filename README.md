# dimensions-scrape
This repo contains modules with a few functions that retrieve Dimensions.ai data given a list of authors. These are a bit specific to needs of my project at the time, but they are concise and easily generalizable to get any data by querying Dimensions.ai.

The module author_papers_from_grants.py takes in a CSV list of researchers and returns a list of article publications from those authors that are supported by the list of grants as written at the beginning of the file. The variables 'author_affils', 'grants' and 'year_range' should be changed to meet the needs of the user.

The module author_query.py takes in a CSV list of researchers and returns an exhaustive list of all article publications from those authors. The variable 'author_affils' should be changed to meet the needs of the user.

Both of these files initialize a session with Dimensions through python's requests module. The authentication for the session happens in the initialize_session() function. The user's login information is expected to be inside of 'login.txt' prior to executing these scripts.
