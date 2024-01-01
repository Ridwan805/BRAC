file3 = open('input3.txt', 'r')
f3 = open('output3.txt', 'w')

s = int(file3.readline())

d = file3.readline().split(' ')
id = [int(x) for x in d]
k = file3.readline().split(' ')
mark = [int(x) for x in k]

for i in range(s):
    min_idx = i
    for j in range(i+1, s):
        if mark[min_idx] < mark[j]:
            min_idx = j

        if mark[min_idx] == mark[j]:
            if id[min_idx] > id[j]:
                min_idx = j

    mark[i], mark[min_idx] = mark[min_idx], mark[i]
    id[i], id[min_idx] = id[min_idx], id[i]

for i in range(s):
    f3.write(f'ID: {id[i]} Mark: {mark[i]}\n')
    
f3.close()
file3.close()
      

