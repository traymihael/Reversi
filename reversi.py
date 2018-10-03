import random
import copy

boad_width = 4
# この個数以下になったら全探索
full_search = 13

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

def change_turn(turn):
    if turn == 'b':
        return 'w'
    else:
        return 'b'


def change_bord(locate_list, location, turn):
    everywhere = [[1, 1],[1, 0],[0, 1],[-1, 1],[-1, 0],[1, -1],[0, -1],[-1, -1]]
    location = list(map(int, location.split('_')))

    locate_list = put_koma(locate_list, location[0], location[1], turn)
    turn_rev = change_turn(turn)

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
    turn_rev = change_turn(turn)

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
    for i in range(boad_width):
        for j in range(boad_width):
            if locate_list_now[i][j] != '-':
                continue
            location = '{}_{}'.format(i, j)

            if check(locate_list_now, location, turn) == 0:
                continue
            place_candidate.append(location)

    return place_candidate

def where_put_full_search_while(locate_list_now, turn, cp_turn):
    global count_full
    next_turn = change_turn(turn)
    result_list = []
    # if cp_turn != 'w':
    #     print(cp_turn)

    place_candidate = get_place_candidate(locate_list_now, turn)

    for i in range(len(place_candidate)):
        location = place_candidate[i]
        locate_list_kari = copy.deepcopy(locate_list_now)
        locate_list_kari = change_bord(locate_list_kari, location, turn)

        place_candidate_next = get_place_candidate(locate_list_kari, next_turn)


        if len(place_candidate_next) == 0:
            place_candidate_next_next = get_place_candidate(locate_list_kari, turn)
            if len(place_candidate_next_next) == 0:
                score = get_final_data(locate_list_kari, cp_turn)
                # result_list.append(score)
            else:
                # print('uuuu')
                score = where_put_full_search_while(locate_list_kari, turn, cp_turn)

        else:
            score = where_put_full_search_while(locate_list_kari, next_turn, cp_turn)
        
        result_list.append(score)
    # print(result_list)
    if len(result_list) == 0:
        result_list.append(get_final_data(locate_list_now, cp_turn))
    else:
        result_list = sorted(result_list)
    if turn == cp_turn:
        # result_list = sorted(result_list.items(), key=lambda x: -x[0])
        # score, location = result_list[0][0], result_list[0][1]
        score_final = result_list[-1]
    else:
        # result_list = sorted(result_list.items(), key=lambda x: x[0])
        # score, location = result_list[0][0], result_list[0][1]
        # try:
        score_final = result_list[0]
        # except:
        #     print(result_list)
        #     print(place_candidate)
        #     a = input()

    count_full += 1
    if count_full % 10000 == 0:
        print(count_full)

    return score_final






def get_final_data(locate_list, cp_turn):
    white, black = 0, 0
    for i in range(len(locate_list)):
        white += locate_list[i].count('w')
        black += locate_list[i].count('b')
    if cp_turn == 'b':
        return black - white
    else:
        return white - black

# 全探索する最強アルゴリズム
def where_put_full_search(locate_list_now, turn):
    cp_turn = copy.deepcopy(turn)
    place_candidate = get_place_candidate(locate_list_now, turn)

    # print(place_candidate)

    # if len(place_candidate) == 0:
    #     return location_put

    result_list = {}
    next_turn = change_turn(turn)

    for i in range(len(place_candidate)):
        location = place_candidate[i]
        locate_list_kari = copy.deepcopy(locate_list_now)
        locate_list_kari = change_bord(locate_list_kari, location, turn)

        score = where_put_full_search_while(locate_list_kari, next_turn, cp_turn)
        result_list[score] = place_candidate[i]
        


        # if len(place_candidate_next) == 0:
        #     score = get_final_data(locate_list_kari, cp_turn)
        #     result_list[score] = place_candidate[i]
        # else:
        #     score, location = where_put_full_search_while(locate_list_kari, place_candidate_next, next_turn, cp_turn)
        #     result_list[score] = place_candidate[i]

    # if turn == cp_turn:
    #     result_list = sorted(result_list.items(), key=lambda x: -x[0])
    #     score, location = result_list[0][0], result_list[0][1]
    # else:
    #     result_list = sorted(result_list.items(), key=lambda x: x[0])
    #     score, location = result_list[0][0], result_list[0][1]
    

    result_list = sorted(result_list.items(), key=lambda x: -x[0])
    print(result_list)
    score, location = result_list[0][0], result_list[0][1]

    print('final is ', score, location)

    return location

def where_put(locate_list_now, turn):
    count_okeru = 0
    for i in range(boad_width):
        count_okeru += locate_list_now[i].count('-')

    if count_okeru <= full_search:
        location_put = where_put_full_search(locate_list_now, turn)
    else:
        location_put = where_put_storategy1(locate_list_now, turn)

    return location_put

# 次の相手のターンで置ける場所が最も少なくなるように
def where_put_storategy1(locate_list_now, turn):
    min_put = boad_width * boad_width
    location_put = ''
    next_turn = change_turn(turn)

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
