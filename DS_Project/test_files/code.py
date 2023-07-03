import sys

j=1
n=int(sys.argv[1])
while(True):
    if(j>n):
        print(j, end = '')
        break
    j=j*2
