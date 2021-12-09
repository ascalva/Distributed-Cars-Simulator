from random            import randint
from typing            import Tuple, Dict
from src.server        import db, app
from src.server.models import User, Obstacle


def is_empty(x: int, y: int) -> bool :
    """
    Check if a space on the board is empty (no cars or obstacles).

    :param x: x-position
    :param y: y-position
    :return:  Boolean indicating if space is empty.
    """
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
    """
    Continuously generates a random position along the board until
    an empty space is found (no cars or obstacles).

    :return: Tuple containing x- and y-position.
    """
    board_height, board_width = app.config["BOARD_DIMS"]

    # Keep generating new position until an empty space is found.
    while True :
        y = randint(0, board_height)
        x = randint(0, board_width)

        if is_empty(x, y) :
            break

    return (x, y)


def proper_move(x_old: int, y_old: int, x_new: int, y_new: int) -> bool :
    """
    Check if car move is accepted, must satisfy:
        - Car only moves one unit in one direction.
        - Car is within boundary.

    :param x_old: Old x-position.
    :param y_old: Old y-position.
    :param x_new: New x-position.
    :param y_new: New y-position.
    :return:      Boolean indicating if move is possible.
    """
    dx = abs(x_new - x_old)
    dy = abs(y_new - y_old)

    # Can only displace a max of one unit in one direction.
    # TODO: Check if board boundary is crossed.
    return (not (dx and dy)) and (dx + dy <= 1)


def get_sensor_data(x: int, y: int) -> Dict[str, bool]:
    """
    Get sensor data about a point on the board.

    :param x: x-position
    :param y: y-position
    :return:  1 if there is 'something', 0 if space is empty.
    """
    return {
        "left"  : not is_empty(x-1, y),
        "right" : not is_empty(x+1, y),
        "up"    : not is_empty(x, y-1),
        "down"  : not is_empty(x, y+1)
    }


def randomly_populate() -> None :
    """
    Randomly populate board with n-number of obstacles, where n is defined
    as INITIAL_OBSTACLE_NUM in the config file.
    """
    for _ in range(app.config["INITIAL_OBSTACLE_NUM"]) :
        x, y = get_empty_space()
        o    = Obstacle(x,y)

        db.session.add(o)

    db.session.commit()

