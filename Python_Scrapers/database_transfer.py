import sqlite3
import os

def get_db():
    '''Connects to sqlite database'''
    db_folder = 'var'
    db_filename = 'makenmodel.sqlite3'

    db_filename = os.path.join(db_folder, db_filename)

    database = sqlite3.connect(str(db_filename))

    database.execute("PRAGMA foreign_keys = ON")

    return database

def transfer_instruction_to_paint():
    pass