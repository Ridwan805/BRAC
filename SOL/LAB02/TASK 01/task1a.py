file1 = open('input1a.txt', 'r')
f1 = open('output1a.txt','w')

line1 = file1.readline().split()

line2 = file1.readline().strip().split()

flag = False
for i in range(int(line1[0])):
      if flag == True:
            break
      for j in range(i+1,int(line1[0])):
            if (int(line2[i]) + int(line2[j])) == int(line1[1]):
                  f1.write(f'{i+1} {j+1}')
                  flag = True
                  break
      


if flag == False:
    f1.write('IMPOSSIBLE')
    
file1.close()
f1.close()