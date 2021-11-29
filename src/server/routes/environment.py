from random            import randint
from typing            import Tuple, Dict
from src.server        import db, app
from src.server.models import User, Obstacle


def is_empty(x: int, y: int) -> bool :
    users = db.session.query(User) \
        .filter(User.position_x == x) \
        .filter(User.position_y == y) \
        .first()

    obstacles = db.session.query(Obstacle) \
        .filter(Obstacle.position_x == x) \
        .filter(Obstacle.position_y == y) \
        .first()

    return (users is None) and (obstacles is None)


def get_empty_space() -> Tuple[int, int]:
    board_height, board_width = app.config["BOARD_DIMS"]

    # Keep generating new position until an empty space is found.
    while True :
        y = randint(0, board_height)
        x = randint(0, board_width)

        if is_empty(x, y) :
            break

    return (x, y)


def proper_move(x_old: int, y_old: int, x_new: int, y_new: int) -> bool :
    dx = abs(x_new - x_old)
    dy = abs(y_new - y_old)

    # TODO: Needs to allow for zero movement.
    return (dx != dy) and (dx + dy == 1)


def get_sensor_data(x: int, y: int) -> Dict[str, bool]:
    return {
        "left"  : is_empty(x-1, y),
        "right" : is_empty(x+1, y),
        "up"    : is_empty(x, y-1),
        "down"  : is_empty(x, y+1)
    }


