import heapq
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


def BFS_Traversal(list,q):
    
    while q != []:            
        temp = heapq.heappop(q)
        queue.append(temp)
        for i in list[temp]:
            if indeg[i] == 1:
                indeg[i] -= 1
                if  indeg[i] == 0:
                     heapq.heappush(q, i)

    


file2 = open('input2.txt', 'r')
f2 = open('output2.txt','w')

v,e = [int(i) for i in file2.readline().split(' ')]

visitedc =  [int(0)]*(v+1)
visited = [int(0)]*(v+1)
graph = [[]for i in range(v+1)]
indeg = [int(0)]*(v+1) 
q = []
queue = []

for i in range(e):
    f,s = [int(i)for i in file2.readline().split(' ')]
    graph[f].append(s)
    indeg[s] = 1

cycleg = False

for i in range(1, v+1):
    if visitedc[i] == 0:
        cycle_wh= Cycle_Detect(graph, i)
        if cycle_wh:
            cycleg = True
            break
    
if cycleg:
    f2.write('Impossible')
else:
    
    for i in range(1,len(indeg)):
        if indeg[i] == 0:
          q.append(i)
    
    
    BFS_Traversal(graph,q)
    
    for i in queue:
        f2.write(f'{i} ')

        

file2.close()
f2.close()