from enum import Enum
from Guess import Accusation
from Guess import Suggestion
from users import User

class Respond(Enum):
    PLAYER = User,
    ACCUSATION = Accusation,
    SUGGESTION = Suggestion,
    TOTAL_PLAYERS = int,
    PLAYER_COUNTER_S = "",
    CHARACTER_MOVE = [User, int, int],
    SINGLE_USER = [],
    CHARACTER_CONNECTED = User
    CHARACTER_MOVE_MSG = ""
    GAME_LOG = []
    LIST_OF_USERS = [User]
    PLAYER_DISCONNECT = User
