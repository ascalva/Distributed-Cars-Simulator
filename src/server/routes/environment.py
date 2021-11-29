from random            import randint
from src.server        import db, app
from src.server.models import User, Obstacle


def is_empty(x, y) :
    users = db.session.query(User) \
        .filter(User.position_x == x) \
        .filter(User.position_y == y) \
        .first()

    obstacles = db.session.query(Obstacle) \
        .filter(Obstacle.position_x == x) \
        .filter(Obstacle.position_y == y) \
        .first()

    return None not in (users, obstacles)


def get_empty_space() :
    board_height, board_width = app.config["BOARD_DIMS"]

    # Keep generating new position until an empty space is found.
    while True :
        y = randint(0, board_height)
        x = randint(0, board_width)

        if is_empty(x, y) :
            break

    return (x, y)


def proper_move(x_old, y_old, x_new, y_new) :
    dx = abs(x_new - x_old)
    dy = abs(y_new - y_old)

    return (dx != dy) and (dx + dy == 1)

