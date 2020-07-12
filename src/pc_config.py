import yaml
import os


# Config File


def read_config_yaml(path=None):
    path = get_config_yaml_path(path)
    assert '~' not in path, 'Tilde shortcut not supported'
    assert os.path.exists(path), 'Config file not found at `{0}`'.format(path)
    with open(path, 'r') as yaml_file:
        yaml_dict = yaml.safe_load(yaml_file)
        return Config(yaml_dict)


def get_config_yaml_path(path):
    if path is not None:
        return path

    possible_paths = [
        './config.yml',
        './config.yaml',
        '../config.yml',
        '../config.yaml',
        './config/config.yml',
        './config/config.yaml',
        '../config/config.yml',
        '../config/config.yaml',
    ]

    for possible_path in possible_paths:
        if os.path.exists(possible_path):
            return possible_path


# Config Structures


class Config:
    yaml_dict = None
    plex_base_url = None
    plex_auth_token = None
    plex_mount_path = None
    plex_builtin_fs_prefix = None
    sections = []

    def __init__(self, yaml_dict):
        self.yaml_dict = yaml_dict
        self.plex_base_url = yaml_dict['plex_base_url']
        self.plex_auth_token = yaml_dict['plex_auth_token']
        self.plex_mount_path = yaml_dict['plex_mount_path']
        self.plex_builtin_fs_prefix = yaml_dict['plex_builtin_fs_prefix']
        self.sections = [ConfigSection(section) for section in yaml_dict['sections']]

    def __str__(self):
        return self.__toString()

    def __toString(self, pad_depth=0):
        header_pad = '\t' * pad_depth
        inner_pad = '\t' * (pad_depth + 1)

        lines = [
            '{0}{1}:\n'.format(header_pad, 'Config'),
            '{0}{1:13} {2}\n'.format(inner_pad, 'Base URL', self.plex_base_url),
            '{0}{1:13} {2}\n'.format(inner_pad, 'Auth Token', self.plex_auth_token),
            '{0}{1:13} {2}\n'.format(inner_pad, 'Mount Path', self.plex_mount_path),
            '{0}{1:13} {2}\n'.format(inner_pad, 'FS Prefix', self.plex_builtin_fs_prefix),
            '{0}{1}:\n'.format(inner_pad, 'Sections'),
            ''.join([section.toString(pad_depth=pad_depth + 2) for section in self.sections]),
        ]

        return ''.join(lines)


class ConfigSection:
    yaml_dict = None
    section_name = None
    collection_tag_prefix = None
    collection_tag_suffix = None

    def __init__(self, yaml_dict):
        self.yaml_dict = yaml_dict
        self.section_name = yaml_dict['section_name']
        self.collection_tag_prefix = yaml_dict['collection_tag_prefix']
        self.collection_tag_suffix = yaml_dict['collection_tag_suffix']

    def __str__(self):
        return self.toString()

    def toString(self, pad_depth=0):
        header_pad = '\t' * pad_depth
        inner_pad = '\t' * (pad_depth + 1)

        lines = [
            '{0}{1}:\n'.format(header_pad, 'Section'),
            '{0}{1:13} {2}\n'.format(inner_pad, 'Name', self.section_name),
            '{0}{1:13} {2}\n'.format(inner_pad, 'Tag Prefix', self.collection_tag_prefix),
            '{0}{1:13} {2}\n'.format(inner_pad, 'Tag Suffix', self.collection_tag_suffix)
        ]

        return ''.join(lines)
