from pc_cli import parse_arguments
from pc_config import read_config_yaml
from pc_log import log_message
from pc_collections import delete_empty_collections, get_proper_collection_tags, apply_collection_tags


# https://github.com/pkkid/python-plexapi
import plexapi.server


def main():
    (config_path, dry_run) = parse_arguments()
    config = read_config_yaml(config_path)

    pms = plexapi.server.PlexServer(config.plex_base_url, config.plex_auth_token)

    log_message('Pre-Apply Actions:', 0)
    delete_empty_collections(pms, log_depth=1)

    for config_section in config.sections:
        section = pms.library.section(config_section.section_name)
        log_message('Processing {0}'.format(config_section.section_name), 0, prepend='\n\n')
        for movie in section.all():
            log_message('Processing {0}'.format(movie.title), 1, prepend='\n\n')
            proper_collection_tags = get_proper_collection_tags(movie, section, config.plex_builtin_fs_prefix, config.plex_mount_path, config_section)
            apply_collection_tags(movie, proper_collection_tags, log_depth=2, do_apply=not dry_run)

    # section4KMovies = pms.library.section('4K Movies')
    # for movie4K in section4KMovies.all():
    #     log_message('Processing {0}'.format(movie4K.title), 0, prepend='\n\n')
    #     proper_collection_tags = get_proper_collection_tags(movie4K, section4KMovies, config.plex_builtin_fs_prefix, config.plex_mount_path)
    #     apply_collection_tags(movie4K, proper_collection_tags, log_depth=1)

    # sectionMovies = pms.library.section('Movies')
    # for movie in sectionMovies.all():
    #     log_message('Processing {0}'.format(movie.title), 0, prepend='\n\n')
    #     proper_collection_tags = get_proper_collection_tags(movie, sectionMovies, config.plex_builtin_fs_prefix, config.plex_mount_path)
    #     apply_collection_tags(movie, proper_collection_tags, log_depth=1)

    log_message('Post-Apply Actions:', 0, prepend='\n\n')
    delete_empty_collections(pms, log_depth=1, do_apply=not dry_run)


if __name__ == '__main__':
    main()
