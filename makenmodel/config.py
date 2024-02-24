'''Configuration file for project'''

import pathlib

APPLICATION_ROOT = '/'

MAKENMODEL_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = pathlib.Path('/var/uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jped', 'gif', 'heic'])

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

DATABASE_FILENAME = MAKENMODEL_ROOT/'var'/'makenmodel.sqlite3'
