import random
import copy

boad_width = 6
# この個数以下になったら全探索
full_search = 11

count_full = 0

def get_initial_place():
    initial_place = [['-' for i in range(boad_width)] for j in range(boad_width)]
    a, b = int(boad_width / 2), int(boad_width / 2) - 1
    initial_place[b][b] = 'w'
    initial_place[a][a] = 'w'
    initial_place[b][a] = 'b'
    initial_place[a][b] = 'b'
    return initial_place

def put_koma(locate_list, x, y, turn):
    locate_list[int(x)][int(y)] = turn
    return locate_list


def get_position():
    position_data = []
    for i in range(boad_width):
        position_data.append([])
        for j in range(boad_width):
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
    for i in range(boad_width):
        for j in range(boad_width):
            if locate_list[i][j] != '-':
                continue
            location = '{}_{}'.format(i, j)
            if check(locate_list, location, turn):
                next_flg += 1
    return next_flg



def print_data(locate_list):
    for i in range(len(locate_list)):
        print(locate_list[i])



def get_place_candidate(locate_list_now, turn):
    place_candidate = []
    fin_flg = 0
    for i in range(boad_width):
        for j in range(boad_width):
            if locate_list_now[i][j] != '-':
                continue
            location = '{}_{}'.format(i, j)

            if check(locate_list_now, location, turn) == 0:
                continue
            place_candidate.append(location)
    if len(place_candidate) == 0:
        fin_flg = 1

    return place_candidate, fin_flg

def where_put_full_search_while(locate_list_now, place_candidate, turn, cp_turn):
    global count_full
    if turn == 'b':
        next_turn = 'w'
    else:
        next_turn = 'b'
    result_list = {}

    for i in range(len(place_candidate)):
        location = place_candidate[i]
        locate_list_kari = copy.deepcopy(locate_list_now)
        locate_list_kari = change_bord(locate_list_kari, location, turn)

        place_candidate_next, fin_flg = get_place_candidate(locate_list_kari, next_turn)


        if fin_flg:
            score = get_final_data(locate_list_kari, cp_turn)
            result_list[score] = location
        else:
            score, location = where_put_full_search_while(locate_list_kari, place_candidate_next, next_turn, cp_turn)
            result_list[score] = location

    if turn == cp_turn:
        result_list = sorted(result_list.items(), key=lambda x: -x[0])
        score, location = result_list[0][0], result_list[0][1]
    else:
        result_list = sorted(result_list.items(), key=lambda x: x[0])
        score, location = result_list[0][0], result_list[0][1]


    count_full += 1
    if count_full % 1000 == 0:
        print(count_full)

    return score, location






def get_final_data(locate_list, cp_turn):
    white, black = 0, 0
    for i in range(len(locate_list)):
        white += locate_list[i].count('w')
        black += locate_list[i].count('b')
    if cp_turn == 'b':
        return black - white
    else:
        return white - black


def where_put_full_search(locate_list_now, turn):
    cp_turn = copy.deepcopy(locate_list_now)

    place_candidate, fin_flg = get_place_candidate(locate_list_now, turn)

    if fin_flg:
        return location_put

    score, location_put = where_put_full_search_while(locate_list_now, place_candidate, turn, cp_turn)
    print('final is ',location_put, score)


    return location_put


def where_put(locate_list_now, turn):
    count_okeru = 0

    for i in range(boad_width):
        count_okeru += locate_list_now[i].count('-')

    if count_okeru <= full_search:
        location_put = where_put_full_search(locate_list_now, turn)
    else:
        min_put = 64
        location_put = ''

        if turn == 'b':
            next_turn = 'w'
        else:
            next_turn = 'b'

        for i in range(boad_width):
            for j in range(boad_width):
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
    width = [_ for _ in range(boad_width)]
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
