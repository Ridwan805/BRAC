import heapq
input_file = open('input.txt', 'r')
output_file = open('output.txt','w')

def heuristic_and_graph(h_n):
    heurist = {}
    gra = {}
    total_lines = h_n.readlines() #reading the lines from the input file
    for each_line in total_lines:
        l = each_line.strip().split()
        heurist.update({l[0]:int(l[1])}) #extracting the heuristic value
        gra.update({l[0]:[]}) #taking the key of the dictionary 
        for i in range(2,len(l),2):
            gra[l[0]] += [[l[i],int(l[i+1])]] #assigning the value(distance and city) to the corresponding keys
    return gra, heurist

def A_star_search(start, end, graph, heuristic):

    pqueue = [] #priority queue
    heapq.heappush(pqueue, [heuristic[start],start]) #assigning the starting node in the priority queue
    parent= {start:None} #assigning the starting parent node to none
    distance = {start: 0} #assigning the starting distance to 0
    

    while pqueue != []:
        hval, name = heapq.heappop(pqueue) #popping the first value
        for node,value in graph[name]: #searching for the child nodes and the distance value
            td = distance[name] + value #calculating distance f(n)
            if node not in distance or td < distance[node]:
               distance[node]= td 
               totalcost = td + heuristic[node] # total cost = h(n) + f(n)
               heapq.heappush(pqueue, [totalcost, node])
               parent[node]= name
    # print(totalcost)
    
    required_path = []
    temp = end
    while temp is not None:
        required_path.append(temp)
        temp = parent.get(temp)
    
    required_path.reverse()

    if required_path[0] != start: 
        output_file.write('No path found')
    else: 
        output_file.write(f"Path: {' -> '.join(required_path)}\nTotal distance: {distance[end]} km")


    # print(required_path)
    # print(parent)
    # print(distant)
    


    # if required_path[0] != start:
    #     print('No path found')
    # else:
    #     print(f"Path: {' -> '.join(required_path[0:])}\nTotal distance: {distance[end]} km")

start = input('Starting point: ')
stop = input('Destintion point: ')
                

Graph, Heuristic=  heuristic_and_graph(input_file)

A_star_search(start,stop,Graph,Heuristic)