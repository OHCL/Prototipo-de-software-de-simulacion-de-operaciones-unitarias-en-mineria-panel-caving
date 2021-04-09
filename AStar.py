# Node Atr: Parent, x, y, heuristics (djikstra, greedy, astar), testing code.
# Astar Atr: mapmatrix, start, end.
'''
-¿Clase constructora para crear nodos?, ¿clase adaptador?.

Mejoras y revisiones:
-Revisar el proceso de las closed list
-Revisar proceso de "ordenado"
'''

class NodeClass():
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position # (rows, columns)

        h_djik = 0
        h_greedy = 0
        h_astar = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return str(self.position)

def sorter (list, atr = "astar"):
    if atr == "astar":
        sorting = sorted(list, key= lambda e: e.h_astar)
    elif atr == "djik":
        sorting = sorted (list, key=lambda e: e.h_djik)
    elif atr == "greedy":
        sorting = sorted (list, key=lambda e: e.h_greedy)

    return sorting

def astar (mapMatrix, start, end):
    open_list = []
    closed_list = []

    start_node = NodeClass(None, start)
    start_node.h_djik = start_node.h_greedy = start_node.h_astar = 0
    end_node = NodeClass (None, end)
    end_node.h_djik = end_node.h_greedy = end_node.h_astar = 0

    open_list.append(start_node)
    counter = 0

    while len(open_list) > 0:
        counter += 1
        open_list = sorter(open_list)
        currentNode = open_list[0]
        print(currentNode.position, currentNode.parent, currentNode.h_djik, currentNode.h_greedy, currentNode.h_astar)


        if currentNode.position == end_node.position:
            path = []
            current = currentNode
            while current is not None:
                path.append (current.position)
                current = current.parent

            print ("Counter:", counter)

            return path[::-1]
        # check = open_list[0].h_greedy
        # print (check)


        newPositions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        setPositions = set()
        for node_position in newPositions:
            setPositions.add((currentNode.position[0]+node_position[0],currentNode.position[1]+node_position[1]))
        #print(setPositions)


        setClosed = set()
        cList = list(map(lambda x: x.position, closed_list))
        setClosed = setClosed.union(set(cList))
        #print (setClosed)
        setFinal = setPositions - setClosed
        #print(setFinal)


        oList = list(map(lambda x: x.position, open_list))
        setOpen = set ()
        setOpen = setOpen.union (set (oList))
        setFinal = setFinal - setOpen


        filter = []
        for node_position in setFinal:
            print (node_position[0], node_position[1], len(mapMatrix) - 1, len(mapMatrix[len(mapMatrix)-1])-1)
            if node_position[0] < 0 or node_position[1] < 0 or node_position[0] > (len(mapMatrix)) - 1 or node_position[1] > (len(mapMatrix[len(mapMatrix)-1])-1):
                continue


            if mapMatrix[node_position[0]][node_position[1]] != 0:
                continue


            newNode = NodeClass(parent=currentNode, position=(node_position[0],node_position[1]))
            newNode.h_djik = currentNode.h_djik + 1
            newNode.h_greedy = (abs(newNode.position[0] - end_node.position[0]) + abs(newNode.position[1] - end_node.position[1]))
            newNode.h_astar = newNode.h_djik + newNode.h_greedy


            open_list.insert(0, newNode)
            #print(newNode.position, newNode.parent, newNode.h_djik, newNode.h_greedy, newNode.h_astar)
            # filter.append(i)
        # print(filter)

        # print(currentNode.position)

        closed_list.append(currentNode)
        open_list.remove(currentNode)



if __name__ == "__main__":
    maze = [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]

    # (y,x)
    start = (0,0)
    end = (9,9)

    route = astar(maze, start, end)
    print (route)

