CREATE_USER_TABLE = '''
        CREATE TABLE IF NOT EXISTS telegram_users
        (ID INTEGER PRIMARY KEY,
        TELEGRAM_ID INTEGER,
        USER_NAME CHAR(30),
        FIRST_NAME CHAR(30),
        LAST_NAME CHAR(30),
        UNIQUE (TELEGRAM_ID)
        )
'''


START_INSERT_USER = '''INSERT OR IGNORE INTO telegram_users VALUES (?,?,?,?,?)'''