# Plex Collections

Automatically apply Plex Collections according to the file system structure and an accompanying Collections.txt file. Warning! This is a destructive operation. Plex Collections will be deleted and created.


# Warning
This tool will destroy all your existing collections! If you have any custom collections that you want preserved, you must store those collection tags in Collections.txt. Learn more about Collections.txt in the Expected File System Layout section.

To see what the tool would do without applying changes, pass the `-d` or `--dry` flag. To apply the changes, run again without `-d` and `--dry`.


# Dependencies

Install dependencies with `pip`.

`pip install -r requirements.txt`

# Usage

```
usage: main.py [-h] [-c CONFIG] [-d]

Automatically apply Plex Collections

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to YAML configuration file
  -d, --dry             Dry Run. If true, show output but do not apply changes
```


# Expected File System Layout

This tool analyzes the file system layout of your Plex library and automatically generates collection tags accordingly. Note, the library name is not included. In addition, the tool generates collection tags for each line inside an accompanying Collections.txt file. Collections.txt should reside next to your video file (eg mkv, mp4, etc.).

Consider this File System Layout. In this example, Collections.txt contains one line indicated in parentehses:

```
/Volumes/MyPlexLibrary # Locally mounted Plex library
    ├── 4K Movies
    │    ├── The Avengers
    │    │    ├── The Avengers
    │    │    │    └── Avengers.mp4
    │    │    └── The Avengers: Infinity War
    │    │         ├── InfinityWar.mp4
    │    │         └── Collectionts.txt (Favorite)
    │    │
    │    └── 1917
    │         ├── 1917.mp4
    │         └── Collectionts.txt (Favorite)
    │
    └── HD Movies
         ├── Star Wars
         │    └── Star Wars - Original Trilogy
         │         ├── Episode IV
         │         │    ├── IV.mp4
         │         │    └── Collections.txt (Best of John Williams)
         │         ├── Episode V
         │         │    └── V.mp4
         │         └── Episode VI
         │              └── VI.mp4
         │
         └── Super 8
              └── Super8.mp4
```

The following collection tags will be generated and applied:

| Movie        | Collection 1 | Collection 2     | Collection 3          |   |
|--------------|--------------|------------------|-----------------------|---|
| Avengers     | The Avengers |                  |                       |   |
| Infinity War | The Avengers | Favorite         |                       |   |
| 1917         | Favorite     |                  |                       |   |
| Episode IV   | Star Wars    | Original Trilogy | Best of John Williams |   |
| Episode V    | Star Wars    | Original Trilogy |                       |   |
| Episode VI   | Star Wars    | Original Trilogy |                       |   |
| Super 8      |              |                  |                       |   |


Star Wars Episode IV gained collections for both of its parent folders as well as its Collections.txt file. However, Super 8 gained no collections since it has no parent folder (aside from the library folder itself) and no Collections.txt


# TV Shows

TV Shows are not currently supported.


# Config File

The Config file provides connection details as well as minor customization settings for your Plex libraries. Reference the included `config.yml` file for details.

The YAML config file is sourced automatically from the following locations:
- ./config.yml
- ./config.yaml
- ../config.yml
- ../config.yaml
- ./config/config.yml
- ./config/config.yaml
- ../config/config.yml
- ../config/config.yaml

Alternatiely, an absolute path can be specified using the `-c` or `--config` arguments.


# plex_builtin_fs_prefix

This is probably confusing. The good news is, there are very easy steps to get this value.

1. Open the Plex web app
2. Go to a library
3. Go to a movie
4. Click `Get Info` on the movie (inside the `...` menu)
5. In the Files box, there is a long file path pointing to the binary video file on the Plex drive
6. Copy everything BEFORE your custom library folder. Your library folder will probably be something like Movies, 4K Movies, XXX Movies, etc.
7. Paste this value into `config.yml` as `plex_builtin_fs_prefix`