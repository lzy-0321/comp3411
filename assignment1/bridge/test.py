import sys
import random

# 定义四个方向的向量
direction = [(0, -1), (-1, 0), (0, 1), (1, 0)]
# 最大桥数限制
max_bridge_num = 3
# 字符到整数的映射，用于不同方向上的桥梁表示
ch_to_int = [{0: 0, '-': 1, '=': 2, 'E': 3, '|': 0, '"': 0, '#': 0},
             {0: 0, '|': 1, '"': 2, '#': 3, '-': 0, '=': 0, 'E': 0}]
# 整数到字符的映射，用于不同方向上的桥梁表示
int_to_ch = [{0: 0, 1: '-', 2: '=', 3: 'E'},
             {0: 0, 1: '|', 2: '"', 3: '#'}]

# 从标准输入读取地图数据
def scan_map():
    text = []
    for line in sys.stdin:
        row = []
        for ch in line:
            n = ord(ch)
            if n >= 48 and n <= 57:  # 数字 '0' 到 '9'
                row.append(n - 48)
            elif n >= 97 and n <= 122:  # 小写字母 'a' 到 'z'
                row.append(n - 87)
            elif ch == '.':
                row.append(0)
        text.append(row)
    return text

# 根据方向和字符获取桥的编码
def get_bridge_code(dir, ch):
    if isinstance(ch, int) and 0 < ch:
        return 0
    return ch_to_int[dir % 2][ch]

# 格式化元素为输出格式
def format(ele):
    if isinstance(ele, int):
        if ele >= 10:
            return chr(ord('a') + ele - 10)
        elif ele == 0:
            return ' '
    return ele

# 打印地图数据
def print_map(data):
    for row in data:
        print(''.join(str(format(cell)) for cell in row))

# 将地图数据转换为元组形式，用于状态记录
def map_2_tuple(data):
    return tuple(tuple(row) for row in data)

# 检查坐标是否在地图范围内
def is_valid(data, i, j):
    n = len(data)
    m = len(data[0])
    return 0 <= i < n and 0 <= j < m

# 获取指定方向上的桥的数量
def get_bridge_num(data, i, j, dir):
    ni = i + direction[dir][0]
    nj = j + direction[dir][1]
    if not is_valid(data, ni, nj):
        return 0
    return get_bridge_code(dir % 2, data[ni][nj])

# 在指定方向上搜索桥梁
# return [桥梁数量, 下一个位置]
def search_direction(data, i, j, dir):
    bnum = get_bridge_num(data, i, j, dir)
    if bnum >= max_bridge_num:
        return [0, (-1, -1)]
    bnch = int_to_ch[dir % 2][bnum]
    ni = i + direction[dir][0]
    nj = j + direction[dir][1]
    while is_valid(data, ni, nj) and data[ni][nj] == bnch:
        ni += direction[dir][0]
        nj += direction[dir][1]
    if not is_valid(data, ni, nj):
        return [0, (-1, -1)]
    if isinstance(data[ni][nj], int) and 0 < data[ni][nj]:
        exist_bn = 0
        for nd in range(4):
            exist_bn += get_bridge_num(data, ni, nj, nd)
        return [min(max_bridge_num - bnum, data[ni][nj] - exist_bn), (ni, nj)]
    return [0, (-1, -1)]

# 添加桥梁并更新地图状态
def add_bridge(data, i, j, dir, num):
    if num == 0:
        return
    bnum = get_bridge_num(data, i, j, dir)
    bnch = int_to_ch[dir % 2][bnum]
    nbnch = int_to_ch[dir % 2][bnum + num]
    ni = i + direction[dir][0]
    nj = j + direction[dir][1]
    while is_valid(data, ni, nj) and data[ni][nj] == bnch:
        data[ni][nj] = nbnch
        ni += direction[dir][0]
        nj += direction[dir][1]

# 计算在特定方向上可以增加的桥梁数量
def potential_bridge_num(data, i, j, dir):
    # 调用 search_direction 函数获取可能增加的桥梁数量
    return search_direction(data, i, j, dir)[0]

# 根据潜在桥梁数量和剩余需求计算最小确定建造的桥梁数量
def get_min_comfirmed_bridges(potential, remain_bn):
    sump = sum(potential)
    min_bridge_list = []
    for p in potential:
        min_bridge_list.append(max(0, remain_bn - sump + p))
    return min_bridge_list

# 添加已确认的桥梁并检查地图的状态
def add_comfirmed_and_check(data, ris):
    correct = True
    valid = True
    no_comfirmed_bridge = True
    for (i, j) in ris:
        exsit = []
        potential = []
        for d in range(4):
            exsit.append(get_bridge_num(data, i, j, d))
            potential.append(potential_bridge_num(data, i, j, d))
        if sum(potential) + sum(exsit) >= data[i][j]:
            min_bridge = get_min_comfirmed_bridges(potential, data[i][j] - sum(exsit))
            for d in range(4):
                if min_bridge[d] > 0:
                    no_comfirmed_bridge = False
                    add_bridge(data, i, j, d, min_bridge[d])
        else:
            valid = False
        if sum(exsit) > data[i][j]:
            valid = False
        elif sum(exsit) < data[i][j]:
            correct = False
        elif sum(exsit) == data[i][j] and (i,j) in ris:
            ris.remove((i,j))
    return [correct, valid, no_comfirmed_bridge]

# 深度优先搜索（DFS）检查地图状态
def dfs_map(data, i, j, vis2):
    if (i,j) in vis2:
        return 0
    vis2[(i,j)] = True

    ret = data[i][j]
    for d in range(4):
        ret -= get_bridge_num(data, i, j, d)
        [potential, (ni, nj)] = search_direction(data, i, j, d)
        if potential > 0:
            ret += dfs_map(data, ni, nj, vis2)
    return ret

# 检查地图是否正确配置
def check_map_right(data, ris):
    dfs_vis = {}
    for (i, j) in ris:
        numsum = dfs_map(data, i, j, dfs_vis)
        if numsum % 2 == 1:
            return False
    return True

# 估算成本，用于启发式搜索
def cost_estimation(num, po):
    if (num, po[0], po[1], po[2], po[3]) in est_mp:
        return est_mp[(num, po[0], po[1], po[2], po[3])]
    if num == 0:
        return 0
    count = 0
    for i in range(4):
        for k in range(1, po[i] + 1):
            if num - k >= 0:
                copied_po = po[:]
                copied_po[i] -= k
                count += cost_estimation(num - k, copied_po) + 1
    est_mp[(num, po[0], po[1], po[2], po[3])] = count
    return count

# 启发式函数，根据成本估算排序未决定的岛屿
def heuristic(data, ris):
    res = []
    for (i, j) in ris:
        exsit = []
        potential = []
        for d in range(4):
            exsit.append(get_bridge_num(data, i, j, d))
            potential.append(potential_bridge_num(data, i, j, d))
        if sum(exsit) == data[i][j]:
            continue
        remain = data[i][j] - sum(exsit)
        cost = cost_estimation(remain, potential)
        res.append((i, j, cost))
    sorted_res = sorted(res, key=lambda x: x[2])
    return [(x[0], x[1]) for x in sorted_res]

# 回溯法搜索解
def backtrack(data, vis, ris):
    # 如果当前状态已经访问过，则返回 False
    if map_2_tuple(data) in vis:
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
    ris = heuristic(data, ris)
    for (i, j) in ris:
        for d in range(4):
            if potential_bridge_num(data, i, j, d) > 0:
                data_tmp = [row[:] for row in data]
                ris_tmp = ris[:]
                add_bridge(data_tmp, i, j, d, 1)
                if backtrack(data_tmp, vis, ris_tmp):
                    return True
    return False


# 主函数，程序入口
if __name__ == '__main__':
    map_data = scan_map()
    # vis is a dictionary to record the visited status of the map
    vis = {}
    # islands is a list to record the positions of the islands
    islands = []
    # est_mp is a dictionary to record the estimated cost of the remaining bridges
    est_mp = {}
    n = len(map_data)
    m = len(map_data[0])
    for i in range(n):
        for j in range(m):
            if isinstance(map_data[i][j], int) and 0 < map_data[i][j]:
                islands.append((i, j))
    backtrack(map_data, vis, islands)
