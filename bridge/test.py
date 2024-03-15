import sys
import random
direction = [(0, -1), (-1, 0), (0, 1), (1, 0)]
max_bridge_num = 3
ch_to_int = [{0: 0, '-': 1, '=': 2, 'E': 3, '|': 0, '"': 0, '#': 0},
             {0: 0, '|': 1, '"': 2, '#': 3, '-': 0, '=': 0, 'E': 0}]
int_to_ch = [{0: 0, 1: '-', 2: '=', 3: 'E'},
             {0: 0, 1: '|', 2: '"', 3: '#'}]



def scan_map():
    text = []
    for line in sys.stdin:
        row = []
        for ch in line:
            n = ord(ch)
            if n >= 48 and n <= 57:  # between '0' and '9'
                row.append(n - 48)
            elif n >= 97 and n <= 122:  # between 'a' and 'z'
                row.append(n - 87)
            elif ch == '.':
                row.append(0)
        text.append(row)

    return text



def get_bridge_code(dir, ch):
    if isinstance(ch, int) and 0 < ch:
        return 0
    return ch_to_int[dir % 2][ch]


def format(ele):
    if isinstance(ele, int):
        if ele >= 10:
            return chr(ord('a') + ele - 10)
        elif ele == 0:
            return ' '
    return ele



def print_map(data):
    for row in data:
        # print(' '.join(str(format(cell)) for cell in row))
        print(''.join(str(format(cell)) for cell in row))

def map_2_tuple(data):
    return tuple(tuple(row) for row in data)

def is_valid(data, i, j):
    n = len(data)
    m = len(data[0])
    if i >= 0 and i < n and j >= 0 and j < m:
        return True
    return False

def get_bridge_num(data, i, j, dir):
    ni = i + direction[dir][0]
    nj = j + direction[dir][1]
    if not is_valid(data, ni, nj):
        return 0
    return get_bridge_code(dir % 2, data[ni][nj])



def search_direction(data, i, j, dir):
    bnum = get_bridge_num(data, i, j, dir)
    if bnum >= max_bridge_num:
        return [0, (-1,-1)]
    bnch = int_to_ch[dir % 2][bnum]
    ni = i + direction[dir][0]
    nj = j + direction[dir][1]
    while is_valid(data, ni, nj) and data[ni][nj] == bnch:
        ni = ni + direction[dir][0]
        nj = nj + direction[dir][1]
    if not is_valid(data, ni, nj):
        return [0, (-1,-1)]
    if isinstance(data[ni][nj], int) and 0 < data[ni][nj]:
        exsit_bn = 0
        for nd in range(0, 4):
            exsit_bn += get_bridge_num(data, ni, nj, nd)
        return [min(max_bridge_num - bnum, data[ni][nj] - exsit_bn), (ni,nj)]
    return [0, (-1,-1)]

def potential_bridge_num(data, i, j, dir):
    return search_direction(data, i, j, dir)[0]

def add_bridge(data, i, j, dir, num):
    if num == 0:
        return
    #print("bridge",i,j,dir,num)
    bnum = get_bridge_num(data, i, j, dir)
    bnch = int_to_ch[dir % 2][bnum]
    nbnch = int_to_ch[dir % 2][bnum + num]
    ni = i + direction[dir][0]
    nj = j + direction[dir][1]
    while is_valid(data, ni, nj) and data[ni][nj] == bnch:
        data[ni][nj] = nbnch
        ni = ni + direction[dir][0]
        nj = nj + direction[dir][1]

def get_min_comfirmed_bridges(potential, remain_bn):
    sump = sum(potential)
    min_bridge_list = []
    for p in potential:
        min_bridge_list.append(max(0, remain_bn - sump + p))
    return min_bridge_list

def add_comfirmed_and_check(data, ris):
    n = len(data)
    m = len(data[0])
    correct = True
    valid = True
    no_comfirmed_bridge = True
    for (i, j) in ris:
        exsit = []
        potential = []
        for d in range(0, 4):
            exsit.append(get_bridge_num(data, i, j, d))
            potential.append(potential_bridge_num(data, i, j, d))
        if sum(potential) + sum(exsit) >= data[i][j]:
            min_bridge = get_min_comfirmed_bridges(potential, data[i][j] - sum(exsit))
            for d in range(0, 4):
                if min_bridge[d] > 0:
                    no_comfirmed_bridge = False
                    add_bridge(data, i, j, d, min_bridge[d])
                    exsit[d] += min_bridge[d]
                    potential[d] -= min_bridge[d]
        else:
            valid = False
        if sum(exsit) > data[i][j]:
            valid = False
        elif sum(exsit) < data[i][j]:
            correct = False
        elif sum(exsit) == data[i][j]:
            if (i,j) in ris:
                ris.remove((i,j))
    return [correct, valid, no_comfirmed_bridge]

def dfs_map(data, i, j, vis2):
    if (i,j) in vis2.keys():
        return 0
    vis2[(i,j)] = True

    ret = data[i][j]
    for d in range(0, 4):
        ret -= get_bridge_num(data, i, j, d)
        [potential, (ni,nj)] = search_direction(data,i,j,d)
        if potential > 0:
            ret += dfs_map(data, ni, nj, vis2)
    if ret < 0:
        print("error")
    return ret


def check_map_right(data, ris):
    dfs_vis = {}
    for (i, j) in ris:
        numsum = dfs_map(data,i, j,dfs_vis)
        if numsum % 2 == 1:
            return False
    return True

def cost_estimation(num, po):
    if (num,po[0],po[1],po[2],po[3]) in est_mp.keys():
        return est_mp[(num,po[0],po[1],po[2],po[3])]
    if num == 0:
        return 0
    count = 0
    for i in range(0,4):
        for k in range(1, po[i]+1):
            if num - k >= 0:
                copied_po = po[:]
                copied_po[i] -= k
                count += cost_estimation(num-k, copied_po) + 1
    est_mp[(num,po[0],po[1],po[2],po[3])] = count
    return count

def heuristic(data, ris):
    res = []
    for (i, j) in ris:
        exsit = []
        potential = []
        for d in range(0, 4):
            exsit.append(get_bridge_num(data, i, j, d))
            potential.append(potential_bridge_num(data, i, j, d))
        if sum(exsit) == data[i][j]:
            continue
        remain = data[i][j]-sum(exsit)
        cost = cost_estimation(remain, potential)
        res.append((i,j,cost))
    #random.shuffle(res)
    #res_xy = [(x[0], x[1]) for x in res]
    #return res_xy
    sorted_res = sorted(res, key=lambda x: x[2])
    sorted_res_xy = [(x[0], x[1]) for x in sorted_res]
    return sorted_res_xy

def backtrack(data, vis, ris):
    if map_2_tuple(data) in vis.keys():
        return False
    vis[map_2_tuple(data)] = True
    while True:
        [correct, valid, no_comfirmed] = add_comfirmed_and_check(data, ris)
        if not valid:
            return False
        if correct:
            print_map(data)
            return True
        if no_comfirmed:
            break
    if not check_map_right(data, ris):
        return False
    #print_map(data)
    #print("--------"+str(len(vis))+"----------")
    ris = heuristic(data, ris)
    for (i, j) in ris:
        dir_list = [0, 1, 2, 3]
        random.shuffle(dir_list)
        for d in dir_list:
            if potential_bridge_num(data, i, j, d) > 0:
                data_tmp = [row[:] for row in data]
                ris_tmp = ris[:]
                add_bridge(data_tmp, i, j, d, 1)
                if backtrack(data_tmp, vis, ris_tmp):
                    return True
    return False


if __name__ == '__main__':
    map = scan_map()
    #print_map(map)
    #print("------------------------")
    vis = {}
    islands = []
    est_mp = {}
    n = len(map)
    m = len(map[0])
    for i in range(0, n):
        for j in range(0, m):
            if isinstance(map[i][j], int) and 0 < map[i][j]:
                islands.append((i,j))
    backtrack(map,vis,islands)
