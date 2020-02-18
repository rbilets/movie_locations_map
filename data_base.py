""" Module to search for closest film locations using database city_coordinates.tsv """

def read_city_coordinates(file):
    '''
    Returns a list of tuples with city coordinates
    '''
    city_coords = []
    with open(file, mode='r', encoding='utf-8') as rf:
        line = rf.readline()
        line = rf.readline()
        while line:
            coordinates = line.strip().split('\t')
            city_coords.append((coordinates[:-2], (coordinates[-2], coordinates[-1])))
            line = rf.readline()
    return city_coords


def get_closest_location(file, lat, lng):
    '''
    Returns closest cities to entered coordinates (Lat, Lng)
    '''
    city_coords = read_city_coordinates(file)
    close_cities = []
    for city in city_coords:
        distance = ((lat - float(city[1][0]))**2 + (lng - float(city[1][1]))**2)**(1/2)
        close_cities.append((city[0], city[1], distance))
    close_cities.sort(key=lambda x: x[2])
    return close_cities


def read_file(file, year):
    '''
    Reads file and returns list of tuples
    with movies and their locations
    '''
    with open(file, mode='r', encoding='utf-8', errors='ignore') as rf:
        location = rf.readline()
        while not location.startswith('"'):
            location = rf.readline()

        movie_locations = []
        while location and not location.startswith('-----'):
            if str(year) in location:
                if '{' in location:
                    movie = location[:location.index('{')].strip()
                    movie_loc = location[location.index('}') + 1:].strip()
                    movie_locations.append((movie, movie_loc))
                    location = rf.readline()
                else:
                    movie = location[:location.index('(')].strip()
                    movie_loc = location[location.index(')') + 1:].strip()
                    movie_locations.append((movie, movie_loc))
                    location = rf.readline()
            else:
                location = rf.readline()

    return movie_locations


def find_movies(loc, coords, year, lat, lng):
    '''
    Returns list of movies filmed near entered coordinates
    '''
    movie_locs = read_file(loc, year)
    close_locs = get_closest_location(coords, lat, lng)
    closest_movies = []

    for close_loc in close_locs:
        for movie_loc in movie_locs:
            if len(closest_movies) == 10:
                break
            else:
                if close_loc[0][1] in movie_loc[1]:
                    closest_movies.append((movie_loc[0], float(close_loc[1][0]), float(close_loc[1][1])))
                    closest_movies = list(set(closest_movies))
    return closest_movies


def prepare_movies_map(loc, coords, year, lat, lng):
    '''
    Adjust movies longitude to perfectly fit on the map screen
    '''
    movies = []
    i = 0
    for movie in find_movies(loc, coords, year, lat, lng):
        movie = list(movie)
        movie[2] += i * 0.0006
        movies.append(movie)
        i += 1
    return movies


def read_capitals(file):
    '''
    Returns a list of tuples with countries capitals
    '''
    capitals = []
    with open(file, mode='r', encoding='utf-8') as rf:
        capital = rf.readline()
        capital = rf.readline()
        while capital:
            capital = capital.strip().split(',')
            capital[2], capital[3] = float(capital[2]), float(capital[3])
            capitals.append(tuple(capital))
            capital = rf.readline()
    return capitals