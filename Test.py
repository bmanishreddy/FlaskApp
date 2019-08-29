lis = [1,4,6,8,4]
sum =0
seen = lis[0]
#print(len(lis))
for i in range(0,len(lis)):
    sum = lis[0]+lis[i]
    if sum == 10:
        print(sum)
    else:
        seen = lis[i]
    #print(lis.index())
