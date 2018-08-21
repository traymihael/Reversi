import random
import copy

def get_initial_place():
    initial_place = [['-' for i in range(8)] for j in range(8)]
    initial_place[3][3] = 'w'
    initial_place[4][4] = 'w'
    initial_place[3][4] = 'b'
    initial_place[4][3] = 'b'
    return initial_place

def put_koma(locate_list, x, y, turn):
    locate_list[int(x)][int(y)] = turn
    return locate_list


def get_position():
    position_data = []
    for i in range(8):
        position_data.append([])
        for j in range(8):
            position_data[-1].append('{}_{}'.format(i, j))
    return position_data

def change_bord(locate_list, location, turn):
    everywhere = [[1, 1],[1, 0],[0, 1],[-1, 1],[-1, 0],[1, -1],[0, -1],[-1, -1]]
    location = list(map(int, location.split('_')))

    locate_list = put_koma(locate_list, location[0], location[1], turn)

    if turn == 'b':
        turn_rev = 'w'
    else:
        turn_rev = 'b'

    for i in range(len(everywhere)):
        direc = everywhere[i]
        locate_now_posi = [location[0] + direc[0], location[1] + direc[1]]
        reversi_locate = []

        while 1:
            try:
                now_color = locate_list[locate_now_posi[0]][locate_now_posi[1]]
            except:
                reversi_locate = []
                break
            if locate_now_posi[0] < 0 or locate_now_posi[1] < 0:
                reversi_locate = []
                break

            if now_color == turn_rev:
                reversi_locate.append(locate_now_posi)
            elif now_color == turn:
                break
            else:
                reversi_locate = []
                break
            locate_now_posi = [locate_now_posi[0] + direc[0], locate_now_posi[1] + direc[1]]

        for j in range(len(reversi_locate)):
            x, y = reversi_locate[j]
            put_koma(locate_list, x, y, turn)


    return locate_list

def change_turn(turn):
    if turn == 'b':
        return 'w'
    else:
        return 'b'

def get_hist(history, location, turn):
    data = '{}_{}'.format(location, turn)
    history.append(data)
    return history

def undo_data(locate_list, history):
    history.pop(-1)
    locate_list_ver2 = get_initial_place()
    for i in range(len(history)):
        location, turn = history[i].rsplit('_', 1)
        locate_list_ver2 = change_bord(locate_list_ver2, location, turn)
    return locate_list_ver2, history

def check(locate_list, location, turn):
    everywhere = [[1, 1], [1, 0], [0, 1], [-1, 1], [-1, 0], [1, -1], [0, -1], [-1, -1]]
    location = list(map(int, location.split('_')))
    check_flg = 0

    if turn == 'b':
        turn_rev = 'w'
    else:
        turn_rev = 'b'

    for i in range(len(everywhere)):
        direc = everywhere[i]
        locate_now_posi = [location[0] + direc[0], location[1] + direc[1]]
        reversi_locate = []

        while 1:
            try:
                now_color = locate_list[locate_now_posi[0]][locate_now_posi[1]]
            except:
                reversi_locate = []
                break
            if locate_now_posi[0] < 0 or locate_now_posi[1] < 0:
                reversi_locate = []
                break

            if now_color == turn_rev:
                reversi_locate.append(locate_now_posi)
            elif now_color == turn:
                break
            else:
                reversi_locate = []
                break
            locate_now_posi = [locate_now_posi[0] + direc[0], locate_now_posi[1] + direc[1]]

        if len(reversi_locate) != 0:
            check_flg += 1

    return check_flg

def check_next(locate_list, turn):
    next_flg = 0
    for i in range(8):
        for j in range(8):
            if locate_list[i][j] != '-':
                continue
            location = '{}_{}'.format(i, j)
            if check(locate_list, location, turn):
                next_flg += 1
    return next_flg



def print_data(locate_list):
    for i in range(len(locate_list)):
        print(locate_list[i])

def where_put(locate_list_now, turn):
    min_put = 64
    location_put = ''

    if turn == 'b':
        next_turn = 'w'
    else:
        next_turn = 'b'

    for i in range(8):
        for j in range(8):
            if locate_list_now[i][j] != '-':
                continue
            location = '{}_{}'.format(i, j)
            locate_list_kari = copy.deepcopy(locate_list_now)

            if check(locate_list_kari, location, turn) == 0:
                continue

            locate_list_kari = change_bord(locate_list_kari, location, turn)
            next_put = check_next(locate_list_kari, next_turn)

            # for k in range(len(locate_list_kari)):
            #     print(locate_list[k])
            # print()

            if next_put < min_put:
                min_put = next_put
                location_put = location
            elif next_put == min_put:
                if random.randrange(2) == 0:
                    min_put = next_put
                    location_put = location


    return location_put


if __name__ == '__main__':
    locate_list = get_initial_place()
    position_data = get_position()
    width = [_ for _ in range(8)]
    turn = 'b'
    print_data(locate_list)
    print()

    location = '5_3'
    locate_list = change_bord(locate_list, location, turn)
    turn = change_turn(turn)
    print_data(locate_list)
    print()

    location = '5_4'
    locate_list = change_bord(locate_list, location, turn)
    turn = change_turn(turn)
    print_data(locate_list)
