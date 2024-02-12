import mariadb
from components.commands import dateFormat


class MariaDB:
    def __init__(self, host: str = '', port: int = 0, username: str = '', password: str = '', db: str = 'db'):
        try:
            self.client = mariadb.connect(
                user=username,
                password=password,
                host=host,
                port=port,
                database=db
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            exit()
        self.cursor = self.client.cursor()
        self.querys = {'humedad': "INSERT INTO db.humedad (value) VALUES (?)",
                       'temperatura': "INSERT INTO db.temperatura (value) VALUES (?)",
                       'presion': "INSERT INTO db.presion (value) VALUES (?)",
                       'compass': "INSERT INTO db.compass (x, y, z) VALUES (?, ?, ?)",
                       'acelerometro': "INSERT INTO db.acelerometro (x, y, z) VALUES (?, ?, ?)",
                       'giroscopio': "INSERT INTO db.giroscopio (roll, pitch, yaw) VALUES (?, ?, ?)"}

    def run_query(self, query, parameters=tuple()):
        self.cursor.execute(query, parameters)
        try:
            data = list(self.cursor)
        except:
            data = list()
        self.client.commit()
        return data

    def select_datetime(self, db, datetimeInit, datetimeEnd):
        # Datetime format YYYY-MM-DD HH:mm:ss
        try:
            columns = self.run_query(f"SHOW COLUMNS FROM db.{db}")
            returnData = {}
            for column in columns:
                returnData[column[0]] = list(item[0] for item in self.run_query(f"SELECT {column[0]}  FROM db.{db} WHERE createdAt >= '{datetimeInit}' AND createdAt <= '{datetimeEnd}'"))
            returnData['createdAt'] = dateFormat(returnData['createdAt'])
            return returnData
        except mariadb.ProgrammingError as ex:
            print(type(ex).__name__)
            return ({"message": str(ex)})