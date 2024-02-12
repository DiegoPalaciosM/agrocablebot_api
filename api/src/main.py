import os

from components.mysql import MariaDB
from api import ApiWeb

def notFound(error):
    return '<h1>Pagina no encontrada - 404</h1>', 404

if __name__ == '__main__':
    hostRP = os.environ['SERVER_HOST']
    database = MariaDB(hostRP, 3306, os.environ['MARIADB_USERNAME'], os.environ['MARIADB_PASSWORD'])
    app = ApiWeb(database)
    app().register_error_handler(404, notFound)
    #app().run(host='0.0.0.0', port=7001, debug=True, threaded=True)
    from waitress import serve
    serve(app(), host='0.0.0.0', port=7001)