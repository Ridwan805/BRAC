def Cycle_Detect(list, selected):
    visitedc[selected] = 1
    
    for adj_node in list[selected]:
        if visitedc[adj_node] == 0:
            cycle = Cycle_Detect(list, adj_node)
            if(cycle):
                return True
            
        elif visitedc[adj_node] == 1:
            return True

    visitedc[selected] = 2
    return False


def DFS_Traversal(list,source):
    visited[source] = 1
    for i in list[source]:
        if visited[i] == 0:
            DFS_Traversal(list,i)
    stack.append(source)



file1a = open('input1a.txt', 'r')
f1a = open('output1a.txt','w')

v,e = [int(i) for i in file1a.readline().split(' ')]

visitedc =  [int(0)]*(v+1)
visited = [int(0)]*(v+1)
graph = [[]for i in range(v+1)]
stack = []

for i in range(e):
    f,s = [int(i)for i in file1a.readline().split(' ')]
    graph[f].append(s)

cycleg = False

for i in range(1, v+1):
    if visitedc[i] == 0:
        cycle_wh= Cycle_Detect(graph, i)
        if cycle_wh == True:
            cycleg = True
            break
    
if cycleg == True:
    f1a.write('Impossible')
else:
    for i in range(1,v+1):
        if visited[i] == 0:
           DFS_Traversal(graph,i)
    
    stack.reverse()
    
    for i in stack:
        f1a.write(f'{i} ')
    

        

file1a.close()
f1a.close()