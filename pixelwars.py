COMMAND_SHOOT = 1
COMMAND_FARM = 2
COMMAND_RAZE = 3
COMMAND_MOVE = 4
COMMAND_DEPLOY = 5

UNIT_EMPTY = 0
UNIT_GRUNT = 1

OWNER_NEUTRAL = 1
OWNER_RED = 2
OWNER_BLUE = 3

STATE_NORMAL = 0
STATE_FARMING_1 = 1
STATE_FARMING_2 = 2
STATE_FARMING_3 = 3
STATE_FARMING_4 = 4

MAX_X = 512
MAX_Y = 512

COMMAND_KIND_BYTE = 0
COMMAND_TARGET_X_FIRST_BYTE = 1
COMMAND_TARGET_X_SECOND_BYTE = 2
COMMAND_TARGET_Y_FIRST_BYTE = 1
COMMAND_TARGET_Y_SECOND_BYTE = 2

TILE_OWNERSHIP_BYTE = 0
TILE_RED_UNIT_KIND_BYTE = 1
TILE_RED_UNIT_STATE_FIRST_BYTE = 2
TILE_RED_UNIT_STATE_SECOND_BYTE = 3
TILE_BLUE_UNIT_KIND_BYTE = 4
TILE_BLUE_UNIT_STATE_FIRST_BYTE = 5
TILE_BLUE_UNIT_STATE_SECOND_BYTE = 6

empty_board = lambda: zeros((MAX_X, MAX_Y), dtype='int64')

def get_byte(number, byte):
    pass

class Command():
    def __init__(self, command_bytes, coords=None):
        self.kind_no = get_byte(command_bytes, COMMAND_KIND_BYTE)
        target_x_first = get_byte(command_bytes, COMMAND_TARGET_X_FIRST_BYTE)
        target_x_second = get_byte(command_bytes, COMMAND_TARGET_X_SECOND_BYTE)
        self.target_x = command_bytes_target_x_first*256 +
                command_bytes_target_x_second
        target_y_first = get_byte(command_bytes, COMMAND_TARGET_Y_FIRST_BYTE)
        target_y_second = get_byte(command_bytes, COMMAND_TARGET_Y_SECOND_BYTE)
        self.target_y = command_bytes_target_y_first*256 +
                command_bytes_target_y_second
        self.coords = coords

class Tile():
    def __init__(self, tile_bytes, coords=None):
        self.ownership = get_byte(tile_bytes, TILE_OWNERSHIP_BYTE)
        self.red_unit_kind_no = get_byte(tile_bytes, TILE_RED_UNIT_KIND_BYTE)
        red_unit_state_fst= get_byte(tile_bytes,
                TILE_RED_UNIT_STATE_FIRST_BYTE)
        red_unit_state_snd= get_byte(tile_bytes,
                TILE_RED_UNIT_STATE_SECOND_BYTE)
        self.red_unit_state = red_unit_state_fst*256 + red_unit_state_snd
        self.blue_unit_kind_no = get_byte(tile_bytes, TILE_BLUE_UNIT_KIND_BYTE)
        blue_unit_state_fst = get_byte(tile_bytes,
                TILE_BLUE_UNIT_STATE_FIRST_BYTE)
        blue_unit_state_snd= get_byte(tile_bytes,
                TILE_BLUE_UNIT_STATE_SECOND_BYTE)
        self.blue_unit_state = red_unit_state_fst*256 + red_unit_state_snd
        self.coords = coords

    def get_bytes(self):
        pass

class UnitKind():
    def __init__(self, name, strength, toughness, shoot_range, move_range,
            farm_duration):
        self.name = name
        self.strength = strength
        self.toughness = toughness
        self.shoot_range = shoot_range
        self.move_range = move_range
        self.farm_duration = farm_duration

UNITS = {
    UNIT_GRUNT : UnitKind(
        name = "Grunt",
        strength = 1,
        toughness = 3,
        shoot_range = 10,
        move_range = 1,
        farm_duration = 5,
        ),
    }

def tile_distance(x1, y1, x2, y2):
    abs(x1 - x2) + abs(y1 - y2)

def iterate(board, red_commands, blue_commands):
    red_shot_counter = empty_board()
    red_move_counter = empty_board()
    blue_shot_counter = empty_board()
    blue_move_counter = empty_board()

    # first, count shots and moves
    for x in xrange(MAX_X):
        for y in xrange(MAX_Y):
            tile = Tile(board[x,y])
            red_command = Command(red_commands[x,y])
            blue_command = Command(blue_commands[x,y])

            for color in ('red', 'blue'):
                if color == 'red':
                    unit_kind_no = tile.red_unit_kind_no
                    shot_counter = red_shot_counter
                    move_counter = red_move_counter
                    command = red_command 
                else:
                    unit_kind_no = tile.blue_unit_kind_no
                    shot_counter = blue_shot_counter
                    move_counter = blue_move_counter
                    command = blue_command

                # if there is no recognized unit, ignore commands
                if unit_kind_no not in UNIT_NO_MAP:
                    continue

                # alias some values for clarity
                unit_kind = UNIT_NO_MAP[unit_kind_no]
                tx = command.target_x
                ty = command.target_y

                # count shots and moves
                if command.kind_no == COMMAND_SHOOT:
                    if tile_distance(x, y, tx, ty) <= unit_kind.shoot_range:
                        shot_counter[tx, ty] += unit_kind.strength
                if red_command.kind_no == COMMAND_MOVE:
                    if tile_distance(x, y, tx, ty) <= unit_kind.move_range: 
                        move_counter[tx, ty] += 1

    # cancel moves that end up on the same tile
    for x in xrange(MAX_X):
        for y in xrange(MAX_Y):


    # remove any units that have been shot above their strength
    for x in xrange(MAX_X):
        for y in xrange(MAX_Y):
            tile = Tile(board[x,y])

            for color in ('red', 'blue'):
                if color == 'red':
                    shot_counter = red_shot_counter
                    unit_kind_no = tile.blue_unit_kind_no
                else:
                    shot_counter = blue_shot_counter
                    unit_kind_no = tile.blue_unit_kind_no     

                if unit_kind_no not in UNIT_NO_MAP:
                    continue

                unit_kind = UNIT_NO_MAP[unit_kind_no]
                if shot_counter[x,y] >= unit_kind.strength:
                    if color == 'red':
                        tile.red_unit_kind_no = UNIT_EMPTY
                        tile.red_unit_state = STATE_NORMAL
                    else:
                        tile.blue_unit_kind_no = UNIT_EMPTY
                        tile.blue_unit_state = STATE_NORMAL

            # changing game state! (TODO: make new game state)
            board[x,y] = tile.get_bytes()
    
    # are too many units deployed?
