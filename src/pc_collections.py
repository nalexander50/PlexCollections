from pc_log import log_message
from pc_path import get_movie_directory_path, remove_year_tags, split_full_path

import os


# Get Collection Tags


def get_proper_collection_tags(movie, section, fs_prefix, plex_mount_path, section_config):
    movie_dir_path = get_movie_directory_path(movie, fs_prefix, plex_mount_path)
    custom_collections = set(get_custom_collections_from_file(movie_dir_path, section_config))
    file_system_collections = set(get_file_system_collections(movie_dir_path, section, plex_mount_path, section_config))
    union = custom_collections.union(file_system_collections)
    return [
        apply_tag_prefix_suffix(
            tag,
            section_config.collection_tag_prefix,
            section_config.collection_tag_suffix
        )
        for tag.strip() in sorted(list(union))
    ]


def get_custom_collections_from_file(movie_dir, section_config):
    file_names = ['Collections.txt', 'collections.txt']
    for file_name in file_names:
        file_path = os.path.join(movie_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as collections_file:
                return [line.strip() for line in collections_file]
    return []


def get_file_system_collections(movie_dir, section, plex_mount_path, section_config):
    path_minus_years = remove_year_tags(movie_dir)
    collections = split_full_path(path_minus_years)
    collections.pop()  # remove movie directory
    collections.remove(section.title)
    for c in split_full_path(plex_mount_path):
        if c in collections:
            collections.remove(c)
    return [collection.strip() for collection in collections]


def apply_tag_prefix_suffix(line, prefix, suffix):
    line = line.strip()
    if prefix is not None:
        line = prefix + line
    if suffix is not None:
        line = line + suffix
    return line


def apply_collection_tags(movie, new_tags, log_depth=0, do_apply=True):
    not_applying_notice = '' if do_apply else ' [NOT APPLIED]'

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
                if do_apply:
                    movie.removeCollection(old_tag)
                log_message('- Removed `{0}`{1}'.format(old_tag, not_applying_notice), log_depth + 1)
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
                if do_apply:
                    movie.addCollection(new_tag)
                log_message('+ Added `{0}`{1}'.format(new_tag, not_applying_notice), log_depth + 1)
            else:
                log_message('~ Skipping `{0}`'.format(new_tag), log_depth + 1)


def delete_empty_collections(server, log_depth=0, do_apply=True):
    not_applying_notice = '' if do_apply else ' [NOT APPLIED]'

    all_collections = server.library.search(libtype='collection')
    empty_collections = list(filter(lambda collection: collection.childCount == 0, all_collections))

    log_message('Deleting Empty Collections:', log_depth)
    if len(empty_collections) == 0:
        log_message('None', log_depth + 1)
    else:
        for empty_collection in empty_collections:
            if do_apply:
                empty_collection.delete()
            log_message('- Deleted `{0}` ({1}){2}'.format(empty_collection.title, empty_collection.childCount, not_applying_notice), log_depth + 1)
