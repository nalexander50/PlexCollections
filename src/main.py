from argparse import ArgumentParser
import os
import re


# https://github.com/pkkid/python-plexapi
import plexapi
import plexapi.server
import plexapi.library
import plexapi.media
import plexapi.video
import plexapi.utils
import plexapi.base


# Command Line Arguments


def parse_arguments():
    parser = ArgumentParser(description='Automatically apply Plex Collections')

    parser.add_argument('base_url', type=str, help='Base URL for Plex Media Server web portal')
    parser.add_argument('auth_token', type=str, help='X-Plex-Token')
    parser.add_argument('plex_path', type=str, help='Path to mounted Plex library in local file system (ex: /Volumes/MyPlexFiles)')
    parser.add_argument('--fs_prefix', type=str, help='File System path prefix before library folders (default /volume1/Plex/)', default='/volume1/Plex/')

    args = parser.parse_args()
    return (args.base_url, args.auth_token, args.plex_path, args.fs_prefix)


# Get Collection Tags


def get_proper_collection_tags(movie, section, fs_prefix, plex_path):
    movie_dir_path = get_movie_directory_path(movie, fs_prefix, plex_path)
    custom_collections = set(get_custom_collections_from_file(movie_dir_path))
    file_system_collections = set(get_file_system_collections(movie_dir_path, section, plex_path))
    union = list(custom_collections.union(file_system_collections))
    union_sorted = sorted(list(union))
    return union_sorted


def get_custom_collections_from_file(movie_dir):
    file_names = ['Collections.txt', 'collections.txt']
    for file_name in file_names:
        file_path = os.path.join(movie_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as collections_file:
                return [line.strip() for line in collections_file]
    return []


def get_file_system_collections(movie_dir, section, plex_path):
    path_minus_years = remove_year_tags(movie_dir)
    collections = split_full_path(path_minus_years)
    collections.pop() # remove movie directory
    collections.remove(section.title)
    for c in split_full_path(plex_path):
        collections.remove(c)
    return collections


# Collection Utilities


def apply_collection_tags(movie, new_tags, log_depth=0):
    old_tags = sorted([collection.tag for collection in movie.collections])
    new_tags = sorted(new_tags)

    log_message('Removing Existing Collections:', log_depth)
    if len(old_tags) == 0:
        log_message('None', log_depth + 1)
    elif old_tags == new_tags:
        log_message('Matching', log_depth + 1)
    else:
        for old_tag in old_tags:
            if old_tag not in new_tags:
                movie.removeCollection(old_tag)
                log_message('- Removed `{0}`'.format(old_tag), log_depth + 1)
            else:
                log_message('~ Skipping `{0}`'.format(old_tag), log_depth + 1)

    log_message('Adding New Collections:', log_depth, prepend="\n")
    if len(new_tags) == 0:
        log_message('None', log_depth + 1)
    elif old_tags == new_tags:
        log_message('Matching', log_depth + 1)
    else:
        for new_tag in new_tags:
            if new_tag not in old_tags:
                movie.addCollection(new_tag)
                log_message('+ Added `{0}`'.format(new_tag), log_depth + 1)
            else:
                log_message('~ Skipping `{0}`'.format(new_tag), log_depth + 1)


def delete_empty_collections(server, log_depth=0):
    all_collections = server.library.search(libtype='collection')
    empty_collections = list(filter(lambda collection: collection.childCount == 0, all_collections))

    log_message('Deleting Empty Collections:', log_depth)
    if len(empty_collections) == 0:
        log_message('None', log_depth + 1)
    else:
        for empty_collection in empty_collections:
            empty_collection.delete()
            log_message('- Deleted `{0}` ({1})'.format(empty_collection.title, empty_collection.childCount), log_depth + 1)


# Print Utilities


def log_message(log, depth, prepend=None):
    pad = '\t' * depth
    if prepend is not None:
        print(prepend + pad + log)
    else:
        print(pad + log)


def print_outline(title, iterable, depth, selector=None):
    title_pad = '\t' * depth
    inner_pad = '\t' * (depth + 1)

    print(title_pad + title + ":")

    if len(iterable) == 0:
        print(inner_pad + 'None')
    else:
        for e in iterable:
            print(inner_pad + str(e if selector is None else selector(e)))


# Assertions


def assert_plex_path(plex_path):
    assert os.path.isdir(plex_path)


# Path Utilities


def get_movie_directory_path(movie, fs_prefix, plex_path):
    location = movie.locations[0]
    reduced_location = reduce_location_path(location, [fs_prefix])
    movie_directory = os.path.split(reduced_location)[0].strip()
    return os.path.join(plex_path, movie_directory).strip()


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


# Main


def main():
    (base_url, auth_token, plex_path, fs_prefix) = parse_arguments()
    
    pms = plexapi.server.PlexServer(base_url, auth_token)

    log_message('Pre-Apply Actions:', 0)
    delete_empty_collections(pms, log_depth=1)
    
    section4KMovies = pms.library.section('4K Movies')
    for movie4K in section4KMovies.all():
        log_message('Processing {0}'.format(movie4K.title), 0, prepend='\n\n')
        proper_collection_tags = get_proper_collection_tags(movie4K, section4KMovies, fs_prefix, plex_path)
        apply_collection_tags(movie4K, proper_collection_tags, log_depth=1)

    sectionMovies = pms.library.section('Movies')
    for movie in sectionMovies.all():
        log_message('Processing {0}'.format(movie.title), 0, prepend='\n\n')
        proper_collection_tags = get_proper_collection_tags(movie, sectionMovies, fs_prefix, plex_path)
        apply_collection_tags(movie, proper_collection_tags, log_depth=1)

    log_message('Post-Apply Actions:', 0, prepend='\n\n')
    delete_empty_collections(pms, log_depth=1)


main()