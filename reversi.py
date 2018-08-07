def get_initial_place():
    initial_place = [['―' for i in range(8)] for j in range(8)]
    initial_place[3][3] = '●'
    initial_place[4][4] = '●'
    initial_place[3][4] = '○'
    initial_place[4][3] = '○'
    return initial_place

def put_koma(locate_list, point_inf):
    y, x, color = point_inf.split()
    y = ord(y) - 97
    if color == 'B':
        color = '●'
    else:
        color = '○'
    locate_list[int(x)][int(y)] = color
    return locate_list
