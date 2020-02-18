""" Module to search for closest filming location using geopy provider """

from geopy.geocoders import Nominatim


def get_location(coordinates):
    '''
    Converts latitude and longitude to physical address
    '''
    geolocator = Nominatim(user_agent='IMDB_map', timeout=3)
    return geolocator.reverse(coordinates, language='en')


def read_file(file, year):
    '''
    Read file and return list of tuples
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


def find_movies_geopy(loc, year, lat, lng):
    '''
    Finds closest movies to your location
    '''
    current_location = str(get_location((lat, lng))).split()
    movies = read_file(loc, year)
    matches = []
    bad_words = {'Street,', 'City', 'District,', 'Oblast,', 'Loop,', 'of', 'Avenue,', 'United', 'States'}

    for movie in movies:
        intersact = set(current_location).intersection(set(movie[1].split()))
        intersact.difference_update(bad_words)
        if len(intersact) > 1:
            matches.append((movie[0], movie[1].strip(), len(intersact)))

    matches = list(set(matches))
    matches.sort(key=lambda x: x[2], reverse=True)
    if len(matches) > 10:
        return matches[:9]
    else:
        return matches


def convert_movie_to_coordinate(loc, year, lat, lng):
    '''
    Converts movies physical addresses to coordinate addresses
    '''
    closest_movies = find_movies_geopy(loc, year, lat, lng)
    geolocator = Nominatim(user_agent='IMDB_map', timeout=3)
    result = []
    for movie in closest_movies:
        location = geolocator.geocode(movie[1])
        try:
            result.append((movie[0], location.latitude, location.longitude))
        except AttributeError:
            pass
    return result


def prepare_movies_map(loc, year, lat, lng):
    '''
    Adjust movies longitude to perfectly fit on the map screen
    '''
    movies = []
    num = 0
    for movie in convert_movie_to_coordinate(loc, year, lat, lng):
        movie = list(movie)
        movie[2] += num * 0.0002
        movies.append(movie)
        num += 1
    return movies