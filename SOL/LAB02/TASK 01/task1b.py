file1b = open('input1b.txt','r')
f1b = open('output1b.txt','w')

line1 = file1b.readline().split()

line2 = file1b.readline().split()

p1 = 0
p2 = len(line2) - 1
flag = False
while p1 < p2 and p1 != p2:
      if flag == True:
            break
      if int(line2[p1]) + int(line2[p2]) < int(line1[1]):
            p1 += 1
      elif int(line2[p1]) + int(line2[p2]) > int(line1[1]):
            p2 -= 1
      else:
            f1b.write(f'{p1+1} {p2+1}')
            flag = True
            
if flag == False:
      f1b.write('Impossible')
file1b.close()
f1b.close()
            