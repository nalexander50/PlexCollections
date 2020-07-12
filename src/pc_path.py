import os
import re


# Path Utilities


def get_movie_directory_path(movie, fs_prefix, plex_mount_path):
    location = movie.locations[0]
    reduced_location = reduce_location_path(location, [fs_prefix])
    movie_directory = os.path.split(reduced_location)[0].strip()
    if movie_directory.startswith('/'):
        movie_directory = movie_directory[1:]
    return os.path.join(plex_mount_path, movie_directory).strip()


def reduce_location_path(location, exclusions):
    s = location
    for excl in exclusions:
        s = s.replace(excl, '')
    return s


def remove_year_tags(input):
    s = input
    s = re.compile(r'\s*\(\d{4}\)').sub('', s)
    s = re.compile(r'\s*\(\d{4}\-\d{4}\)').sub('', s)
    return s.strip()


def split_full_path(input):
    comps = []
    working = input
    while working != '' and working != '/':
        remain, take = os.path.split(working)
        comps.insert(0, take)
        working = remain
    return comps
