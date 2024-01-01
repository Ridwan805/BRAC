file4 = open('input4.txt','r')
f4 = open('output4.txt','w')


v, e = [int(i)for i in file4.readline().split(' ')]
visited = [0 for i in range(v+1)]

list = [[]for i in range(v+1)]

for i in range(e):
    f, t = [int(i)for i in file4.readline().split(' ')]
    list[f].append(t)


def Cycle_Detect(list, selected):
    visited[selected] = 1
    
    for i in list[selected]:
        if visited[i] == 0:
            cycle = Cycle_Detect(list, i)
            if cycle == True :
                return True
            
        elif visited[i] == 1:
            return True

    visited[selected] = 2
    return False

cycleg = False

for i in range(1, v+1):
    if visited[i] == 0:
        cycle_wh= Cycle_Detect(list, i)
        if cycle_wh == True:
            cycleg = True
            break
    
if cycleg:
    f4.write('YES')
else:
    f4.write("NO")

file4.close()
f4.close()