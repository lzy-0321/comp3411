from nodeDefs import node, waterNode as watN, islandNode as islN, valueDefs as vd

grid = {}

def nodeInit(map, nrow, ncol):
    code = ".123456789abc"
    for i in range(len(map)):
        for j in range(len(map[i])):
            if  code[map[i][j]] == '.':
                # initialise a water node
                tempNode = watN.WaterNode(i, j)
            elif map[i][j] == vd.A_DEF:
                tempNode = islN.IslandNode(i, j, 10)
            elif map[i][j] == vd.B_DEF:
                tempNode = islN.IslandNode(i, j, 11)
            elif map[i][j] == vd.C_DEF:
                tempNode = islN.IslandNode(i, j, 12)
            else:
                # initialise an island node
                tempNode = islN.IslandNode(i, j, map[i][j])
            # assign node to tempNode
            grid[(i, j)] = tempNode
            # print(grid[(i, j)].getCurrCapacity())
            # # grid[(i, j)].callCheck()
        print("\n")
        # we can print grid here for now
    islNodesNeighbours(grid, nrow, ncol)
    # return grid of all nodes
    return grid

# just a setter for all island nodes to have neighbours; also put neighbouring water nodes in adj list or smth. or not.
# or in a queue. whichever works
def islNodesNeighbours(grid, nrow, ncol):
    for i in range(nrow):
        for j in range(ncol):
            if isinstance(grid[(i, j)], islN.IslandNode):
                findNeighbours(grid[i, j], grid, nrow, ncol)

# finds the neighbours accordingly
def findNeighbours(object, grid, nrow, ncol):
    # initializations
    row, col = object.row, object.col
    # checking all 4 sides
    above = row
    below = row
    left = col
    right = col

    # list of neighbours to add to adjList
    neighbourList = []

    # append if island exists
    # LEFT ISLAND
    for i in range(left, -1, -1):
        # same case
        if i in [col, col - 1]:
            pass
        elif isinstance(grid[(row, i)], islN.IslandNode):
            # make it a tuple ?
            neighbourList.append([grid[(row, i)], "horizontal"])
            break
    # RIGHT ISLAND
    for i in range(right, ncol):
        # case same
        if i in [col, col + 1]:
            pass
        elif isinstance(grid[(row, i)], islN.IslandNode):
            neighbourList.append([grid[(row, i)], "horizontal"])
            break
    # UP ISLAND
    for i in range(above, -1, -1):
        # same case
        if i in [row, row - 1]:
            pass
        elif isinstance(grid[(i, col)], islN.IslandNode):
            # print("the thing up is in: ", above, col)
            neighbourList.append([grid[(i, col)], "vertical"])
            break
    # DOWN ISLAND
    for i in range(below, nrow):
        # edge case
        if i in [row, row + 1]:
            pass
        elif isinstance(grid[(i, col)], islN.IslandNode):
            # print("the thing down is in: ", below, col, "and is: ", grid[(i, col)])
            neighbourList.append([grid[(i, col)], "vertical"])
            break
    # sort List over here ? -> based on island Capacity
    neighbourList = sorted(neighbourList, key=lambda x: x[0].maxCapacity)

    # # print out the neighbour adjacency list
    # object.printAdjList() 

    # append to adjList
    appendStack(object, neighbourList)

# TODO: append to Stack: also from Sophie's code
def appendStack(object, neighbours):
    # print(object.getCurrCapacity(), "is the current island as of now")

    for i in range(len(neighbours)):
        # print("Islands nearby: ", neighbours[i][0].maxCapacity, "and type of connection: ", neighbours[i][1])
        # Only including island neighbours
        object.putStack(neighbours[i])

    print("STACK DONE!")