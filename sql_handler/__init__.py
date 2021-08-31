import mysql.connector
import dotenv
from pprint import pprint

dotenv.load_dotenv()
config = dotenv.dotenv_values()


class SqlHelper:
    def __init__(self, database=None, debug=False):
        connection_config = {
            "host": config.get("DB_HOST"),
            "user": config.get("DB_USER"),
            "passwd": config.get("DB_PASSWORD")
        }
        if database:
            connection_config.setdefault("database", database)
        self.connector = mysql.connector.connect(**connection_config)
        self.cursor = self.connector.cursor()
        self.debug = debug

    def close(self):
        self.cursor.fetchall()
        self.connector.commit()
        try:
            self.cursor.close()
        except mysql.connector.errors.InternalError:
            pass
        try:
            self.connector.close()
        except mysql.connector.errors.InternalError:
            pass

    def execute_query(self, query, params=(), commit=False, debug=False):
        if self.debug or debug:
            print(query % params)
        self.cursor.execute(query, params)
        if commit:
            self.connector.commit()

    def fetch_all(self):
        results = self.cursor.fetchall()
        columns = self.cursor.description
        if results:
            return [dict(zip(row, columns)) for row in results]
        return []

    def fetch_one(self):
        results = self.cursor.fetchone()
        columns = self.cursor.description
        if results:
            return dict(zip(results, columns))
        return None


class SqlContext:
    def __init__(self, database=None):
        if database:
            self.helper = SqlHelper(database=database)
        else:
            self.helper = SqlHelper()

    def __enter__(self):
        return self.helper

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.helper.close()


if __name__ == '__main__':
    helper = SqlHelper()
    helper.execute_query("SELECT * FROM `adoption_agency`.`pets`")
    pprint(helper.fetch_all())
