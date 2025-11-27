import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values


class PgConnector:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PgConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self, dbname, user, password, host, port):
        self._connection = None
        self.db_config = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }

    def connect(self):
        if not self._connection:
            self._connection = psycopg2.connect(**self.db_config)

    def disconnect(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def insert_data(self, schema_name, table_name, data, batch_size=10000):
        self.connect()
        cursor = self._connection.cursor()
        columns = data[0].keys()

        insert_query = sql.SQL("INSERT INTO {}.{}({}) VALUES %s").format(
            sql.Identifier(schema_name),
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns))
        )
        values = [[item[col] for col in columns] for item in data]

        for i in range(0, len(values), batch_size):
            batch = values[i:i + batch_size]
            psycopg2.extras.execute_values(cursor, insert_query, batch)
        self._connection.commit()
        cursor.close()

    def execute_query(self, query, params=None):
        self.connect()
        cursor = self._connection.cursor()
        cursor.execute(query, params)
        self._connection.commit()
        cursor.close()

    def get_data(self, table_name_or_query):
        self.connect()
        cursor = self._connection.cursor()

        if " " not in table_name_or_query:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name_or_query))
        else:
            query = sql.SQL(table_name_or_query)

        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        return result