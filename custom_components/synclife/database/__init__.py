from peewee import SqliteDatabase


def db_init(db_path: str) -> SqliteDatabase:
    db: SqliteDatabase = SqliteDatabase(db_path)
    db.connect()
    return db
