from server.instance import server
from resource import bike, police


if __name__ == '__main__':
    server.init_db()
    server.run()
