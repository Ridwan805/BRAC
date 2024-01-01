f1b = open("output2b.txt", "w")
f1b.write("Now the file has more content!\n")
file1b = open('input1b.txt', 'r')
line = int(file1b.readline())
for i in range(line):
    cal = file1b.readline().strip('calculate ')
    cal = cal.strip('\n')
    if '+' in cal:
        l = cal.split('+')
        res = int(l[0]) + int(l[1])
        f1b.write(f"The result of {cal} is {res}\n")  
    elif '-' in cal:
        l = cal.split('-')
        res = int(l[0]) - int(l[1]) 
        f1b.write(f"The result of {cal} is {res}\n")  
    elif '*' in cal:
        l = cal.split('*')
        res = int(l[0]) * int(l[1])  
        f1b.write(f"The result of {cal} is {res}\n")  
    elif '/' in cal:
        l = cal.split('/')
        res = int(l[0]) / int(l[1])  
        f1b.write(f"The result of {cal} is {res}\n")
f1b.close()
file1b.close()