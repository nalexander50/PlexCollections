from argparse import ArgumentParser


# Command Line Arguments


def parse_arguments():
    parser = ArgumentParser(description='Automatically apply Plex Collections')
    parser.add_argument('-c', '--config', type=str, help='Path to YAML configuration file', default=None)
    parser.add_argument('-d', '--dry', help='Dry Run. If true, show output but do not apply changes', action='store_true')

    args = parser.parse_args()
    return (None if args.config is None else args.config.strip(), args.dry)
