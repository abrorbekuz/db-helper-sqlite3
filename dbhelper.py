import sqlite3
import logging

class Result:
    def __init__(self, result):
        self.result = result
    
    def __getitem__(self, idx):
        if self.exists():
            return self.result[0][idx]
        return None

    def __str__(self):
        return str(self.result)
    
    def All(self):
        return self.result

    def exists(self):
        return len(self.result) > 0

    

class DB_HELPER:
    def __init__(self, db_name):
        self.db_name = db_name
        self.logger = logging.getLogger(__name__)
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)

    def condecon(func):
        def wrapper(self, sql, params=None):
            c = self.conn.cursor()
            results = func(self, sql, params, c)
            c.close()
            return results
        return wrapper

    @condecon
    def execute_query(self, sql, params=None, cursor=None):
        try:
            cursor.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            self.logger.error(str(e), exc_info=True)
            self.conn.rollback()

    @condecon
    def database_query(self, sql, params=None, cursor=None):
        if cursor is None:
            self.logger.warn("[cursor none]")
            return
        cursor.execute(sql, params)
        results = cursor.fetchall()
        return Result(results)

    @condecon
    def many_database_query(self, sql, params=None, cursor=None):
        try:
            cursor.executemany(sql, params)
            self.conn.commit()
        except Exception as e:
            self.logger.error(str(e), exc_info=True)
            self.conn.rollback()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn is not None:
            self.conn.close()